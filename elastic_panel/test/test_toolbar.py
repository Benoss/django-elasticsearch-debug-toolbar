# -*- coding: utf-8 -*-
import unittest

from django.conf import settings
settings.configure()

from elastic_panel import panel

class ImportTest(unittest.TestCase):
    def test_input(self):
        panel.ElasticQueryInfo("GET", "asdasd", "asdasd", "{}", 200, "adssad", 1)
        panel.ElasticQueryInfo("GET", "asdasd", "asdasd", "", 200, "adssad", 1)
        panel.ElasticQueryInfo("GET", "asdasd", "asdasd", None, 200, "adssad", 1)
        panel.ElasticQueryInfo("GET", "asdasd", "asdasd", "{'asddsa': 'é'}", 200, "adssad", 1)
        panel.ElasticQueryInfo("GET", "asdasd", "asdasd", b"{'asddsa': 'asddasds'}", 200, "adssad", 1)
                                                      


if __name__ == '__main__':
    unittest.main()
