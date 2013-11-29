"""
LiveTest - Like WebTest, but on a live site.

Setup an app to test against with just a hostname:

>>> import livetest
>>> app = livetest.TestApp('pypi.python.org')

Make requests just like WebTest:

>>> resp = app.get('/pypi')

Grab forms:

>>> resp.forms # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
{0: <webtest.Form object at 0x...>,
 1: <webtest.Form object at 0x...>,
 u'searchform': <webtest.Form object at 0x...>}
>>> form = resp.forms[0]
>>> form.fields # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
{u'term': [<webtest.Text object at 0x...>],
 u':action': [<webtest.Hidden object at 0x...>],
 u'submit': [<webtest.Submit object at 0x...>]}

Submit forms:

>>> form['term'] = 'python testing'
>>> resp = form.submit()

Test stuff in the response:

>>> resp.mustcontain('livetest', 'Index', 'Package')
>>> resp.status
'200 OK'

"""

__author__ = 'storborg@mit.edu'
__version__ = '0.6'


from livetest.app import TestApp
