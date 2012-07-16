#coding=utf-8

import tornado.web
from . import BaseHandler
import hashlib
from .utils import username_validator, email_validator


class SignupHandler(BaseHandler):
    def get(self):
        if self.current_user:
            self.redirect(self.get_argument('next', '/'))
        self.render('account/signup.html')

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
            self.render('account/signup.html')
            return
        password = hashlib.sha1(password + username.lower()).hexdigest()
        self.db.members.insert({
            'name': username,
            'name_lower': username.lower(),
            'password': password,
            'email': email,
            'website': '',
            'description': '',
            'role': 1,  # TODO:send mail.
            'block': [],
            'like': [],  # topics
            'follow': [],  # users
            'favorite': []  # nodes

        })
        self.set_secure_cookie('user', password, expires_days=30)
        self.redirect(self.get_argument('next', '/'))


class SigninHandler(BaseHandler):
    def get(self):
        if self.current_user:
            self.redirect(self.get_argument('next', '/'))
        self.render('account/signin.html')

    def post(self):
        if self.current_user:
            self.redirect(self.get_argument('next', '/'))
        username = self.get_argument('username', '').lower()
        password = self.get_argument('password', None)
        if not (username and password):
            self.flash('Please fill the required field')
        password = hashlib.sha1(password + username).hexdigest()
        member = self.db.members.find_one({'name_lower': username,
                                           'password': password})
        if not member:
            self.flash('Invalid account or password')
            self.render('account/signin.html')
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
        self.render('account/settings.html')

    @tornado.web.authenticated
    def post(self):
        website = self.get_argument('website', '')
        description = self.get_argument('description', '')
        if len(description) > 1500:
            self.flash("The description is too lang")
        self.db.members.update({'_id': self.current_user['_id']},
                {'$set': {'website': website, 'description': description}})
        self.flash('Saved successfully', type='success')
        self.redirect('/account/settings')


class ChangePasswordHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self):
        old_password = self.get_argument('old_password', None)
        new_password = self.get_argument('new_password', None)
        new_password2 = self.get_argument('new_password2', None)
        if not (old_password and new_password and new_password2):
            self.flash('Please fill the required field')
        if new_password != new_password2:
            self.flash("Password doesn't match")
        password = hashlib.sha1(old_password + self.current_user['name_lower'])
        if password != self.current_user['password']:
            self.flash('Invalid password')
        if self.messages:
            self.render('account/settings.html')
            return
        password = hashlib.sha1(new_password + self.current_user['name_lower'])
        self.db.members.update({'_id': self.current_user['_id']},
                {'$set': {'password': password}})
        self.set_secure_cookie('user', password, expires_days=30)
        self.flash('Saved successfully', type='success')
        self.redirect('/account/settings')

handlers = [
    (r'/account/signup', SignupHandler),
    (r'/account/signin', SigninHandler),
    (r'/account/signout', SignoutHandler),
    (r'/account/settings', SettingsHandler),
    (r'/account/password', ChangePasswordHandler),
]
