#coding=utf-8

from common import BaseHandler
from tornado.web import authenticated
import oauth2 as oauth
import twitter_oauth

class TwitterOauthHandler(BaseHandler):

    @authenticated
    def get(self):
        try:
            verifier = self.get_argument('oauth_verifier')
        except:
            oauth_token,oauth_token_secret = getoauth(self.application.consumer_key,self.application.consumer_secret)
            user = self.get_current_user()
            user['oauth_token'] = oauth_token
            user['oauth_token_secret'] = oauth_token_secret
            self.db.users.save(user)
            self.redirect('http://twitter.com/oauth/authorize?oauth_token=%s' % oauth_token)
        else:
            user = self.get_current_user()
            token = oauth.Token(user['oauth_token'],
                            user['oauth_token_secret'])
            token.set_verifier(verifier)

            client = oauth.Client(oauth.Consumer(self.application.consumer_key,self.application.consumer_secret), token)

            resp, content = client.request('http://twitter.com/oauth/access_token', "POST")
            access_token = dict(_parse_qsl(content))

            oauth_token = access_token['oauth_token']
            oauth_token_secret = access_token['oauth_token_secret']

            user['oauth_token'] = oauth_token
            user['oauth_token_secret'] = oauth_token_secret
            user['twitter_bind'] = True
            user['twitter-sync'] = True

            self.db.users.save(user)
            self.redirect('/setting')



def getoauth(consumer_key,consumer_secret):
    consumer = oauth.Consumer(consumer_key, consumer_secret)
    client = oauth.Client(consumer)
    resp, content = client.request('http://twitter.com/oauth/request_token', "GET")
    if resp['status'] != '200':
        raise Exception('Invalid response %s' % resp['status'])
    request_token = dict(_parse_qsl(content))
    return request_token['oauth_token'],request_token['oauth_token_secret']

def _parse_qsl(url):
    param = {}
    for i in url.split('&'):
        p = i.split('=')
        param.update({p[0]:p[1]})
    return param

class TwitterNotBindHandler(BaseHandler):
    def post(self):
        user = self.get_current_user()
        del user['oauth_token'],user['oauth_token_secret'],user['twitter-sync']
        user['twitter_bind'] = False
        self.db.users.save(user)
        self.redirect('/setting')

class TweetHandler(BaseHandler):
    def post(self):
        user = self.get_current_user()
        api = twitter_oauth.Api(self.application.consumer_key,self.application.consumer_secret, user['oauth_token'], user['oauth_token_secret'])
        api.post_update(tweet=self.get_argument('tweet'))