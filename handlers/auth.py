#coding=utf-8

from . import BaseHandler


class SignupHandler(BaseHandler):
    def get(self):
        self.render('auth_signup.html')

    def post(self):
        pass


class SigninHandler(BaseHandler):
    def get(self):
        self.render('auth_signup.html')

    def post(self):
        pass


class SignoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie('user')
        self.redirect(self.get_argument('next', '/'))


class SettingsHandler(BaseHandler):
    def get(self):
        self.render('auth_settings.html')

    def post(self):
        pass


class ChangePasswordHandler(BaseHandler):
    def get(self):
        self.render('auth_password.html')

    def post(self):
        pass


handlers = [
    (r'/auth/signup', SignupHandler),
    (r'/auth/signin', SigninHandler),
    (r'/auth/signout', SignoutHandler),
    (r'/auth/settings', SettingsHandler),
    (r'/auth/password', ChangePasswordHandler),
]
