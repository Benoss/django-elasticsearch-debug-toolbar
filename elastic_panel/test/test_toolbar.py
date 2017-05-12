# -*- coding: utf-8 -*-
import unittest

from django.conf import settings
settings.configure()

from elastic_panel import panel


class ElasticQueryInfo:
    def __init__(self, method, full_url, path, body, status_code, response, duration):
        if not body:
            self.body = ''  # Python 3 TypeError if None
        else:
            self.body = _pretty_json(body)
            if isinstance(self.body, bytes):
                self.body = self.body.decode('ascii','ignore')
        self.method = method
        self.full_url = full_url
        self.path = path
        self.status_code = status_code
        self.response = _pretty_json(response)
        self.duration = round(duration * 1000, 2)
        self.hash = hashlib.md5("{}{}".format(self.full_url.encode('ascii', 'ignore'), self.body.encode('ascii', 'ignore'))).hexdigest()

class ImportTest(unittest.TestCase):
    def test_input(self):
        panel.ElasticQueryInfo("GET", "asdasd", "asdasd", "{}", 200, "adssad", 1)
        panel.ElasticQueryInfo("GET", "asdasd", "asdasd", "", 200, "adssad", 1)
        panel.ElasticQueryInfo("GET", "asdasd", "asdasd", None, 200, "adssad", 1)
        panel.ElasticQueryInfo("GET", "asdasd", "asdasd", "{'asddsa': 'é'}", 200, "adssad", 1)
        panel.ElasticQueryInfo("GET", "asdasd", "asdasd", b"{'asddsa': 'asddasds'}", 200, "adssad", 1)
                                                      


if __name__ == '__main__':
    unittest.main()
