import httplib
import urlparse

import webtest
from webtest import utils

from six.moves import http_cookiejar


conn_classes = {
    'http': httplib.HTTPConnection,
    'https': httplib.HTTPSConnection
}


class TestApp(webtest.TestApp):

    def __init__(self, host, scheme='http', relative_to=None,
                 extra_environ=None, use_unicode=True, cookiejar=None,
                 parser_features=None):
        self.host = host
        self.relative_to = relative_to
        self.conn = {}
        self._load_conn(scheme)
        self.extra_environ = {}
        self.cookiejar = cookiejar or http_cookiejar.CookieJar()
        self.reset()

    def _load_conn(self, scheme):
        if scheme in conn_classes:
            self.conn[scheme] = conn_classes[scheme](self.host)
        else:
            raise ValueError("Scheme '%s' is not supported." % scheme)

    def _do_httplib_request(self, req):
        "Convert WebOb Request to httplib request."
        headers = dict((name, val) for name, val in req.headers.iteritems()
                       if name != 'Host')
        if req.scheme not in self.conn:
            self._load_conn(req.scheme)

        conn = self.conn[req.scheme]
        conn.request(req.method, req.path_qs, req.body, headers)

        webresp = conn.getresponse()
        res = webtest.TestResponse()
        res.status = '%s %s' % (webresp.status, webresp.reason)
        res.body = webresp.read()
        res.headerlist = webresp.getheaders()
        res.errors = ''
        return res

    def do_request(self, req, status, expect_errors):
        """
        Override webtest.TestApp's method so that we do real HTTP requests
        instead of WSGI calls.
        """
        # set request cookies
        self.cookiejar.add_cookie_header(utils._RequestCookieAdapter(req))

        res = self._do_httplib_request(req)

        # Set these attributes for consistency with webtest.
        res.request = req
        res.test_app = self

        if not expect_errors:
            self._check_status(res.status_int, res)
            self._check_errors(res)

        # merge cookies back in
        self.cookiejar.extract_cookies(
            utils._ResponseCookieAdapter(res),
            utils._RequestCookieAdapter(req)
        )

        return res


def goto(self, href, method='get', **args):
    """
    Monkeypatch the TestResponse.goto method so that it doesn't wipe out the
    scheme and host.
    """
    scheme, host, path, query, fragment = urlparse.urlsplit(href)
    # We
    fragment = ''
    href = urlparse.urlunsplit((scheme, host, path, query, fragment))
    href = urlparse.urljoin(self.request.url, href)
    method = method.lower()
    assert method in ('get', 'post'), (
        'Only "get" or "post" are allowed for method (you gave %r)'
        % method)
    if method == 'get':
        method = self.test_app.get
    else:
        method = self.test_app.post
    return method(href, **args)

webtest.TestResponse.goto = goto
