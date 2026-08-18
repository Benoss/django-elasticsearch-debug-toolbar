import hashlib
import json
import threading

from debug_toolbar.panels import Panel
from debug_toolbar.utils import get_stack_trace, render_stacktrace
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from elasticsearch.connection.base import Connection


class ThreadCollector:
    """Collects queries only between enable and disable, per thread.

    log_request_success is patched process-wide, so without the enabled
    window every Elasticsearch query in any thread that once served a
    toolbar request would accumulate forever (issue #7).
    """

    def __init__(self):
        self.data = threading.local()

    def collect(self, item):
        collection = getattr(self.data, "collection", None)
        if collection is not None:
            collection.append(item)

    def get_collection(self):
        return getattr(self.data, "collection", None) or []

    def enable_collection(self):
        self.data.collection = []

    def disable_collection(self):
        self.data.collection = None


# Patching of the original elasticsearch log_request
old_log_request_success = Connection.log_request_success
collector = ThreadCollector()


def patched_log_request_success(self, method, full_url, path, body, status_code, response, duration):
    collector.collect(ElasticQueryInfo(method, full_url, path, body, status_code, response, duration))
    old_log_request_success(self, method, full_url, path, body, status_code, response, duration)


Connection.log_request_success = patched_log_request_success


def _pretty_json(data):
    # pretty JSON in tracer curl logs
    try:
        return json.dumps(json.loads(data), sort_keys=True, indent=2, separators=(",", ": "))
    except (ValueError, TypeError):
        # non-json data or a bulk request
        return data


class ElasticQueryInfo:
    def __init__(self, method, full_url, path, body, status_code, response, duration):
        if not body:
            self.body = ""  # Python 3 TypeError if None
        else:
            self.body = _pretty_json(body)
            if isinstance(self.body, bytes):
                self.body = self.body.decode("ascii", "ignore")
        self.method = method
        self.full_url = full_url
        self.path = path
        self.status_code = status_code
        self.response = _pretty_json(response)
        self.duration = round(duration * 1000, 2)
        self.hash = hashlib.md5(
            self.full_url.encode("ascii", "ignore") + self.body.encode("ascii", "ignore")
        ).hexdigest()
        self.stacktrace = get_stack_trace(skip=1)


class ElasticDebugPanel(Panel):
    """
    Panel that displays queries made by Elasticsearch backends.
    """

    name = "Elasticsearch"
    template = "elastic_panel/elastic_panel.html"
    has_content = True
    total_time = 0
    nb_duplicates = 0
    nb_queries = 0

    @property
    def nav_title(self):
        return _("Elastic Queries")

    @property
    def nav_subtitle(self):
        default_str = f"{self.nb_queries} queries {self.total_time:.2f}ms"
        if self.nb_duplicates > 0:
            default_str += f" {self.nb_duplicates} DUPE"
        return default_str

    @property
    def title(self):
        return self.nav_title

    def process_request(self, request):
        collector.enable_collection()
        return super().process_request(request)

    def generate_stats(self, request, response):
        records = collector.get_collection()
        self.total_time = 0
        self.nb_duplicates = 0

        hashs = set()
        for record in records:
            self.total_time += record.duration
            if record.hash in hashs:
                self.nb_duplicates += 1
            hashs.add(record.hash)

        self.nb_queries = len(records)

        collector.disable_collection()
        # Debug-toolbar >= 5 serializes stats to JSON and renders panel
        # content from the deserialized copy, so only plain data survives.
        self.record_stats(
            {
                "records": [
                    {
                        "method": record.method,
                        "full_url": record.full_url,
                        "path": record.path,
                        "status_code": record.status_code,
                        "body": record.body,
                        "response": record.response,
                        "duration": record.duration,
                        "hash": record.hash,
                        "stacktrace": str(render_stacktrace(record.stacktrace)),
                    }
                    for record in records
                ],
                "debug": settings.DEBUG,
            }
        )
