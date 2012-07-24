#coding=utf-8

import time
import hashlib
import tornado.web
import tornado.locale
from bson.objectid import ObjectId
from . import BaseHandler
from .utils import username_validator, email_validator


class SignupHandler(BaseHandler):
    def get(self):
        if self.current_user:
            self.redirect(self.get_argument('next', '/'))
        self.render('account/signup.html')

    def post(self):
        self.verify_ayah()
        username = self.get_argument('username', None)
        email = self.get_argument('email', '').lower()
        password = self.get_argument('password', None)
        password2 = self.get_argument('password2', None)
        if not (username and email and password and password2):
            self.flash('Please fill the required field')
        if password != password2:
            self.flash("Password doesn't match")
        if username and not username_validator.match(username):
            self.flash('Username is invalid')
        if email and not email_validator.match(email):
            self.flash('Not a valid email address')
        if username and \
           self.db.members.find_one({'name_lower': username.lower()}):
            self.flash('This username is already registered')
        if email and self.db.members.find_one({'email': email}):
            self.flash('This email is already registered')
        if self.messages:
            self.render('account/signup.html')
            return
        password = hashlib.sha1(password + username.lower()).hexdigest()
        role = 1
        if not self.db.members.count():
            role = 3
        self.db.members.insert({
            'name': username,
            'name_lower': username.lower(),
            'password': password,
            'email': email,
            'website': '',
            'description': '',
            'created': time.time(),
            'language': self.settings['default_locale'],
            'role': role,  # TODO:send mail.
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
        self.verify_ayah()
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
        self.render('account/settings.html', locales=self.application.locales)

    @tornado.web.authenticated
    def post(self):
        website = self.get_argument('website', '')
        description = self.get_argument('description', '')
        language = self.get_argument('language')
        if len(description) > 1500:
            self.flash("The description is too lang")
        self.db.members.update({'_id': self.current_user['_id']}, {'$set': {
                'website': website,
                'description': description,
                'language': language
            }})
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


class LikedHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        topics = self.current_user['like']
        count = len(topics)
        p = int(self.get_argument('p', 1))
        perpage = self.settings['topics_per_page']
        topics = topics[(p - 1) * perpage:p * perpage]
        topics = [self.get_topic(x) for x in topics]
        self.render('account/liked.html', topics=topics, count=count, p=p,
            perpage=perpage)


class FavoritedHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        topics = self.db.topics.find({
            'node': {'$in': self.current_user['favorite']}
        }, sort=[('last_reply_time', -1)])
        topics_count = topics.count()
        p = int(self.get_argument('p', 1))
        self.render('account/favorited.html', topics=topics,
            topics_count=topics_count, p=p)


class FollowedHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        topics = self.db.topics.find({
            'author': {'$in': self.current_user['follow']}
        }, sort=[('last_reply_time', -1)])
        topics_count = topics.count()
        p = int(self.get_argument('p', 1))
        self.render('account/followed.html', topics=topics,
            topics_count=topics_count, p=p)


class NotificationsHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        p = int(self.get_argument('p', 1))
        notis = self.db.notifications.find({
            'to': self.current_user['name_lower']
        }, sort=[('created', -1)])
        notis_count = notis.count()
        per_page = self.settings['notifications_per_page']
        notis = notis[(p - 1) * per_page:p * per_page]
        self.render('account/notifications.html', notis=notis,
            notis_count=notis_count, p=p)


class NotificationsClearHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.db.notifications.remove({'to': self.current_user['name_lower']})
        self.redirect('/')


class NotificationsRemoveHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, id):
        self.db.notifications.remove({'_id': ObjectId(id)})
        self.redirect(self.get_argument('next', '/account/notifications'))


handlers = [
    (r'/account/signup', SignupHandler),
    (r'/account/signin', SigninHandler),
    (r'/account/signout', SignoutHandler),
    (r'/account/settings', SettingsHandler),
    (r'/account/password', ChangePasswordHandler),
    (r'/account/followed', FollowedHandler),
    (r'/account/liked', LikedHandler),
    (r'/account/favorited', FavoritedHandler),
    (r'/account/notifications', NotificationsHandler),
    (r'/account/notifications/clear', NotificationsClearHandler),
    (r'/account/notifications/(\w+)/remove', NotificationsRemoveHandler),
]
