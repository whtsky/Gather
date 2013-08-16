from tornado.web import HTTPError, RequestHandler

from raven.contrib.tornado import SentryMixin as _SentryMixin


class RequestHandler(_SentryMixin, RequestHandler):
    def log_exception(self, typ, value, tb):
        if isinstance(value, HTTPError) and value.status_code in [403, 404]:
            RequestHandler.log_exception(self, typ, value, tb)
        else:
            super(RequestHandler, self).log_exception(typ, value, tb)

    def get_sentry_user_info(self):
        user = self.current_user
        data = user or {}
        return {
            'sentry.interfaces.User': data
        }

    def get_sentry_data_from_request(self):
        """
        Extracts the data required for 'sentry.interfaces.Http' from the
        current request being handled by the request handler

        :param return: A dictionary.
        """
        data = super(RequestHandler, self).get_sentry_data_from_request()
        data['sentry.interfaces.Http']['ip'] = self.request.remote_ip
        return data
