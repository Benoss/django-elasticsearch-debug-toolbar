# -*- coding: utf-8 -*-
import unittest

from django.conf import settings
settings.configure()

from debug_toolbar.toolbar import DebugToolbar
from django.http import HttpResponse
from django.test import RequestFactory
from elasticsearch.connection import Connection
from elastic_panel import panel


class ImportTest(unittest.TestCase):
    def test_input(self):
        panel.ElasticQueryInfo("GET", "asdasd", "asdasd", "{}", 200, "adssad", 1)
        panel.ElasticQueryInfo("GET", "asdasd", "asdasd", "", 200, "adssad", 1)
        panel.ElasticQueryInfo("GET", "asdasd", "asdasd", None, 200, "adssad", 1)
        panel.ElasticQueryInfo("GET", "asdasd", "asdasd", "{'asddsa': 'é'}", 200, "adssad", 1)
        panel.ElasticQueryInfo("GET", "asdasd", "asdasd", b"{'asddsa': 'asddasds'}", 200, "adssad", 1)


class PanelTests(unittest.TestCase):
    def setUp(self):
        self.get_response = lambda request: HttpResponse()
        self.request = RequestFactory().get('/')
        self.toolbar = DebugToolbar(self.request, self.get_response)
        self.panel = panel.ElasticDebugPanel(self.toolbar, self.get_response)

    def test_recording(self, *args):
        response = self.panel.process_request(self.request)
        Connection().log_request_success("GET", "asdasd", "asdasd", "{}", 200, "adssad", 1)
        self.assertIsNotNone(response)

        self.panel.generate_stats(self.request, response)
        stats = self.panel.get_stats()
        self.assertIn('records', stats)
        self.assertEqual(len(stats['records']), 1)


if __name__ == '__main__':
    unittest.main()
