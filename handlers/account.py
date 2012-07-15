#coding=utf-8

import tornado.web
from . import BaseHandler
import re
import hashlib

username_validator = re.compile(r'^[a-zA-Z0-9]+$')
email_validator = re.compile(r'^.+@[^.].*\.[a-z]{2,10}$', re.IGNORECASE)


class SignupHandler(BaseHandler):
    def get(self):
        if self.current_user:
            self.redirect(self.get_argument('next', '/'))
        self.render('account_signup.html')

    def post(self):
        username = self.get_argument('username', None)
        email = self.get_argument('email', '').lower()
        password = self.get_argument('password', None)
        password2 = self.get_argument('password2', None)
        if not (username and email and password and password2):
            self.flash('Please fill the required field')
        if password != password2:
            self.flash("Password doesn't match")
        if not username_validator.match(username):
            self.flash('Username is invalid')
        if not email_validator.match(email):
            self.flash('Not a valid email address')
        if self.db.members.find_one({'name_lower': username.lower()}):
            self.flash('This username is already registered')
        if self.db.members.find_one({'email': email}):
            self.flash('This email is already registered')
        if self.messages:
            self.render('account_signup.html')
            return
        password = hashlib.sha1(password + username.lower()).hexdigest()
        self.db.members.insert({
            'name': username,
            'name_lower': username.lower(),
            'password': password,
            'email': email,
            'website': '',
            'description': '',
            'locale': 'zh_CN-CN',
            'role': 1,  # TODO:send mail.
            'block': [],
            'star': [],
            })
        self.set_secure_cookie('user', password, expires_days=30)
        self.redirect(self.get_argument('next', '/'))


class SigninHandler(BaseHandler):
    def get(self):
        if self.current_user:
            self.redirect(self.get_argument('next', '/'))
        self.render('account_signin.html')

    def post(self):
        username = self.get_argument('username', '').lower()
        password = self.get_argument('password', None)
        if not (username and password):
            self.flash('Please fill the required field')
        password = hashlib.sha1(password + username).hexdigest()
        member = self.db.members.find_one({'name_lower': username,
                                           'password': password})
        if not member:
            self.flash('Invalid account or password')
            self.render('account_signin.html')
            return
        self.set_secure_cookie('user', password, expires_days=30)
        self.redirect(self.get_argument('next', '/'))


class SignoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie('user')
        self.redirect(self.get_argument('next', '/'))


class SettingsHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render('account_settings.html')

    @tornado.web.authenticated
    def post(self):
        pass


class ChangePasswordHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render('account_password.html')

    @tornado.web.authenticated
    def post(self):
        pass

handlers = [
    (r'/account/signup', SignupHandler),
    (r'/account/signin', SigninHandler),
    (r'/account/signout', SignoutHandler),
    (r'/account/settings', SettingsHandler),
    (r'/account/password', ChangePasswordHandler),
]
