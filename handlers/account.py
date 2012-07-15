#coding=utf-8

from . import BaseHandler
import re

username_check = re.compile(u'(\w{1,25})')


class SignupHandler(BaseHandler):
    def get(self):
        self.render('account_signup.html')

    def post(self):
        pass


class SigninHandler(BaseHandler):
    def get(self):
        self.render('account_signup.html')

    def post(self):
        pass


class SignoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie('user')
        self.redirect(self.get_argument('next', '/'))


class SettingsHandler(BaseHandler):
    def get(self):
        self.render('account_settings.html')

    def post(self):
        pass


class ChangePasswordHandler(BaseHandler):
    def get(self):
        self.render('account_password.html')

    def post(self):
        pass


handlers = [
    (r'/account/signup', SignupHandler),
    (r'/account/signin', SigninHandler),
    (r'/account/signout', SignoutHandler),
    (r'/account/settings', SettingsHandler),
    (r'/account/password', ChangePasswordHandler),
]
