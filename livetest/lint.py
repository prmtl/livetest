from webtest.lint import check_content_type
from webtest.lint import check_headers
from webtest.lint import check_status


def lint_response(res):
    check_status(res.status)
    check_headers(res.headerlist)
    check_content_type(res.status, res.headerlist)
