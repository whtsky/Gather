import tornado.web

from raven.contrib.tornado import SentryMixin as _SentryMixin


class RequestHandler(_SentryMixin, tornado.web.RequestHandler):
    def send_error(self, status_code=500, **kwargs):
        if status_code == 404:  # Don't log to sentry when 404
            super(tornado.web.RequestHandler, self).send_error(
                status_code, **kwargs
            )
        else:
            super(_SentryMixin, self).send_error(status_code, **kwargs)
