import importlib
import json
import unittest
from unittest import mock

import django

django.setup()


from debug_toolbar.toolbar import DebugToolbar  # noqa: E402
from django.http import HttpResponse  # noqa: E402
from django.test import (
    RequestFactory,  # noqa: E402
    TestCase,
)
from elasticsearch.connection import Connection  # noqa: E402

from elastic_panel import panel  # noqa: E402


class VersionTest(TestCase):
    def test_version_comes_from_package_metadata(self):
        import elastic_panel

        self.assertNotEqual(elastic_panel.__version__, "unknown")

    def test_version_falls_back_when_package_is_not_installed(self):
        import elastic_panel

        with mock.patch("importlib.metadata.version", side_effect=importlib.metadata.PackageNotFoundError):
            self.assertEqual(importlib.reload(elastic_panel).__version__, "unknown")

        self.assertNotEqual(importlib.reload(elastic_panel).__version__, "unknown")


class ImportTest(TestCase):
    def test_input(self):
        panel.ElasticQueryInfo("GET", "asdasd", "asdasd", "{}", 200, "adssad", 1)
        panel.ElasticQueryInfo("GET", "asdasd", "asdasd", "", 200, "adssad", 1)
        panel.ElasticQueryInfo("GET", "asdasd", "asdasd", None, 200, "adssad", 1)
        panel.ElasticQueryInfo("GET", "asdasd", "asdasd", "{'asddsa': 'é'}", 200, "adssad", 1)
        panel.ElasticQueryInfo("GET", "asdasd", "asdasd", b"{'asddsa': 'asddasds'}", 200, "adssad", 1)


class PrettyJsonTest(TestCase):
    def test_valid_json_is_indented(self):
        self.assertEqual(panel._pretty_json('{"a": 1}'), '{\n  "a": 1\n}')

    def test_json_keys_are_sorted(self):
        pretty = panel._pretty_json('{"b": 2, "a": 1}')
        self.assertLess(pretty.index('"a"'), pretty.index('"b"'))

    def test_invalid_json_is_returned_unchanged(self):
        self.assertEqual(panel._pretty_json("not json"), "not json")

    def test_none_is_returned_unchanged(self):
        self.assertIsNone(panel._pretty_json(None))

    def test_apostrophes_are_not_mangled(self):
        self.assertEqual(panel._pretty_json('{"name": "it\'s"}'), '{\n  "name": "it\'s"\n}')


class QueryInfoTest(TestCase):
    def _info(self, **overrides):
        kwargs = {
            "method": "GET",
            "full_url": "http://es:9200/idx/_search",
            "path": "/idx/_search",
            "body": '{"query": {"match_all": {}}}',
            "status_code": 200,
            "response": '{"took": 1}',
            "duration": 0.1234,
        }
        kwargs.update(overrides)
        return panel.ElasticQueryInfo(**kwargs)

    def test_duration_is_milliseconds(self):
        self.assertEqual(self._info(duration=0.1234).duration, 123.4)

    def test_same_url_and_body_share_hash(self):
        self.assertEqual(self._info().hash, self._info().hash)

    def test_different_body_changes_hash(self):
        self.assertNotEqual(self._info().hash, self._info(body='{"query": {"ids": []}}').hash)

    def test_bytes_body_is_decoded(self):
        info = self._info(body=b'{"a": 1}')
        self.assertIsInstance(info.body, str)


class PanelTests(TestCase):
    def setUp(self):
        self.get_response = lambda request: HttpResponse()
        self.request = RequestFactory().get("/")
        self.toolbar = DebugToolbar(self.request, self.get_response)
        self.panel = panel.ElasticDebugPanel(self.toolbar, self.get_response)
        self.response = self.panel.process_request(self.request)

    def _record_query(self, body='{"query": {"match_all": {}}}'):
        Connection().log_request_success(
            "GET", "http://es:9200/idx/_search", "/idx/_search", body, 200, '{"took": 1}', 0.1
        )

    def test_recording(self, *args):
        self._record_query()
        self.assertIsNotNone(self.response)

        self.panel.generate_stats(self.request, self.response)
        stats = self.panel.get_stats()
        self.assertIn("records", stats)
        self.assertEqual(len(stats["records"]), 1)
        self.assertIn("test_toolbar", stats["records"][0]["stacktrace"])

    def test_content_renders_recorded_query(self):
        self._record_query()
        self.panel.generate_stats(self.request, self.response)

        content = self.panel.content
        self.assertIn("GET 200 /idx/_search", content)
        self.assertIn("match_all", content)
        self.assertIn("test_toolbar", content)

    def test_nav_subtitle_counts_queries_and_duplicates(self):
        self._record_query()
        self._record_query()
        self._record_query(body='{"query": {"ids": []}}')
        self.panel.generate_stats(self.request, self.response)

        self.assertEqual(self.panel.nav_subtitle, "3 queries 300.00ms 1 DUPE")

    def test_stats_survive_json_round_trip(self):
        # Debug-toolbar >= 5 stores panel stats as JSON and renders panel
        # content from the deserialized copy; anything json.dumps cannot
        # handle is silently stringified and renders as empty fields.
        self._record_query()
        self.panel.generate_stats(self.request, self.response)

        record = json.loads(json.dumps(self.panel.get_stats()))["records"][0]
        self.assertEqual(record["method"], "GET")
        self.assertEqual(record["path"], "/idx/_search")
        self.assertEqual(record["status_code"], 200)
        self.assertEqual(record["duration"], 100.0)
        self.assertIn("match_all", record["body"])
        self.assertIn("test_toolbar", record["stacktrace"])

    def test_title(self):
        self.assertEqual(str(self.panel.title), "Elastic Queries")

    def test_content_toggles_use_native_details(self):
        self._record_query()
        self.panel.generate_stats(self.request, self.response)

        content = self.panel.content
        self.assertEqual(content.count("<details>"), 3)
        self.assertIn("<summary>Show Json Body</summary>", content)
        self.assertIn("<summary>Show Json Response</summary>", content)
        self.assertIn("<summary>Show Stacktrace</summary>", content)

    def test_content_without_queries_explains_itself(self):
        self.panel.generate_stats(self.request, self.response)

        self.assertIn("No Elastic queries were recorded", self.panel.content)

    def test_queries_outside_a_panel_cycle_do_not_accumulate(self):
        # Once a pooled worker thread has served one toolbar-enabled request,
        # queries from later non-toolbar requests on the same thread must not
        # pile up in the thread-local collection (issue #7).
        self._record_query()
        self.panel.generate_stats(self.request, self.response)

        self._record_query()
        self.assertEqual(panel.collector.get_collection(), [])

    def test_process_request_clears_leftover_records(self):
        self._record_query()
        self.panel.process_request(self.request)
        self.panel.generate_stats(self.request, self.response)

        self.assertEqual(len(self.panel.get_stats()["records"]), 0)


if __name__ == "__main__":
    unittest.main()
