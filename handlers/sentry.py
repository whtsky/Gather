from tornado import web
import logging

from raven.contrib.tornado import SentryMixin as _SentryMixin


class RequestHandler(_SentryMixin, web.RequestHandler):
    def log_exception(self, typ, value, tb):
        if isinstance(value, web.HTTPError) and value.status_code == 404:
            super(RequestHandler, self).log_exception(typ, value, tb)
        else:
            web.RequestHandler.log_exception(typ, value, tb)
