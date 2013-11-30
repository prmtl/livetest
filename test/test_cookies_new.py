import unittest

from livetest import TestApp


class TestCookies(unittest.TestCase):

    def setUp(self):
        self.testapp = TestApp('httpbin.org')

    def test_cookie_roundtrip(self):
        self.testapp.get('/cookies/set?lorem=ipsum')
        self.testapp.get('/cookies/set?hakuna=matata')

        response = self.testapp.get('/cookies')
        cookies = response.json['cookies']

        self.assertDictEqual(
            cookies,
            {
                'lorem': 'ipsum',
                'hakuna': 'matata',
            }
        )

        self.testapp.get('/cookies/delete?lorem')

        response = self.testapp.get('/cookies')
        cookies = response.json['cookies']

        self.assertDictEqual(
            cookies,
            {
                'hakuna': 'matata',
            }
        )
