from tornado import web

from raven.contrib.tornado import SentryMixin as _SentryMixin


class RequestHandler(_SentryMixin, web.RequestHandler):
    def log_exception(self, typ, value, tb):
        if isinstance(value, web.HTTPError) and value.status_code == 404:
            web.RequestHandler.log_exception(self, typ, value, tb)
        else:
            super(RequestHandler, self).log_exception(typ, value, tb)

    def get_sentry_user_info(self):
        """
        Data for sentry.interfaces.User

        Default implementation only sends `is_authenticated` by checking if
        `tornado.web.RequestHandler.get_current_user` tests postitively for on
        Truth calue testing
        """
        user = self.current_user
        data = {
            'is_authenticated': True if user else False
        }
        if user:
            data['name'] = user['name']
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
