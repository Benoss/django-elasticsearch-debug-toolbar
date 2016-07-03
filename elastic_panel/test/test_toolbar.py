import unittest

from django.conf import settings
settings.configure()

from elastic_panel import panel


class ImportTest(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
