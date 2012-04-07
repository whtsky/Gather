#coding=utf-8

from common import BaseHandler
from tornado.web import authenticated,asynchronous
from tornado import escape
from tornado.auth import TwitterMixin

class TwitterOauthHandler(BaseHandler, TwitterMixin):

    @authenticated
    @asynchronous
    def get(self):
        if self.get_argument('oauth_token', None):
            self.get_authenticated_user(self._on_auth)
        else:
            self.authorize_redirect()

    def _on_auth(self, twitter_user):
        if not twitter_user:
            self.write('Twitter auth failed')
            self.finish()
            return
        user = self.current_user
        user['access_token'] = escape.json_encode(twitter_user['access_token'])
        user['twitter'] = escape.json_encode(twitter_user['username'])
        user['twitter_bind'] = True

        self.db.users.save(user)
        self.redirect('/setting')

class TwitterNotBindHandler(BaseHandler):
    def get(self):
        user = self.current_user
        user['twitter_bind'] = False
        self.db.users.save(user)
        self.redirect('/setting')

class TweetHandler(BaseHandler, TwitterMixin):
    @authenticated
    def post(self):
        user = self.current_user
        self.twitter_request(
            '/statuses/update',
            post_args={'status': self.get_argument('tweet','')},
            access_token=user['access_token'],
            callback=self._on_post)
    def _on_post(self, entry):
        if not entry:
            self.finish('fail')
        else:
            self.finish('ok')