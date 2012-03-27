#coding=utf-8

from common import BaseHandler
from auth import hashpassword
import urlparse, base64
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
    def get(self):
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

class TwitterProxyHandler(BaseHandler):

    def get(self,path):
        self.do_proxy('GET',path)

    def post(self,path):
        self.do_proxy('POST',path)

    def do_proxy(self,method,path):
        username,password = parse_auth_header(self.request.headers)
        password = hashpassword(username,password)
        user = self.db.users.find_one({'username':username,'password':password,'twitter_bind':True})
        client = oauth.Client(oauth.Consumer(self.application.consumer_key,self.application.consumer_secret),
            oauth.Token(user['oauth_token'], user['oauth_token_secret']))
        new_url,new_path = conver_url(path)
        if new_path == '/' or new_path == '':
            self.write('')
            return
        _,content = client.request(new_url,method,body=self.request.body,headers=self.request.headers)
        self.write(content)

def parse_auth_header(headers):
    username = None
    password = None

    if 'Authorization' in headers :
        auth_header = headers['Authorization']
        auth_parts = auth_header.split(' ')
        user_pass_parts = base64.b64decode(auth_parts[1]).split(':')
        username = user_pass_parts[0]
        password = user_pass_parts[1]

    return username, password

def conver_url(orig_url):
    (scm, netloc, path, params, query, _) = urlparse.urlparse(orig_url)

    path_parts = path.split('/')

    if path_parts[1] == 'api' or path_parts[1] == 'search':
        sub_head = path_parts[1]
        path_parts = path_parts[2:]
        path_parts.insert(0,'')
        new_path = '/'.join(path_parts).replace('//','/')
        new_netloc = sub_head + '.twitter.com'
    elif path_parts[1].startswith('search'):
        new_path = path
        new_netloc = 'search.twitter.com'
    else:
        new_path = path
        new_netloc = 'twitter.com'

    new_url = urlparse.urlunparse(('https', new_netloc, new_path.replace('//','/'), params, query, ''))
    return new_url, new_path