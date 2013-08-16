import tornado.web

from raven.contrib.tornado import SentryMixin as _SentryMixin


class RequestHandler(_SentryMixin, tornado.web.RequestHandler):
    def send_error(self, status_code=500, **kwargs):
        if status_code == 404:  # Don't log to sentry when 404
            tornado.web.RequestHandler.send_error(
                self, status_code, **kwargs
            )
        else:
            _SentryMixin.send_error(self, status_code, **kwargs)
