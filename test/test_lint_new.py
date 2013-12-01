import unittest

from livetest import TestApp
from webtest import AppError


class TestLinter(unittest.TestCase):

    def setUp(self):
        self.testapp = TestApp('httpbin.org')

    def test_no_error_when_no_error_status(self):
        self.testapp.get('/status/303')

    def test_no_error_when_we_get_expected_status(self):
        self.testapp.get('/status/403', status=403)

    def test_error_when_we_get_unexpected_status(self):
        with self.assertRaises(AppError):
            self.testapp.get('/status/403', status=200)

    def test_error_when_error_status(self):
        with self.assertRaises(AppError):
            self.testapp.get('/status/403')
