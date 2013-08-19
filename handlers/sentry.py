from tornado.web import HTTPError
from tornado.web import RequestHandler as _RequestHandler

from raven.contrib.tornado import SentryMixin as _SentryMixin


class RequestHandler(_SentryMixin, _RequestHandler):
    def log_exception(self, typ, value, tb):
        if isinstance(value, HTTPError) and value.status_code in [403, 404]:
            _RequestHandler.log_exception(self, typ, value, tb)
        else:
            _SentryMixin.log_exception(self, typ, value, tb)

    def get_sentry_user_info(self):
        user = self.current_user
        data = user or {}
        return {
            'sentry.interfaces.User': {
                "name": user.get("name", ""),
                "email": user.get("email", "")
            }
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
