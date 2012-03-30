#coding=utf-8

from tornado.web import authenticated
from common import BaseHandler
from config import i_consumer_key,i_consumer_secret
from imguring import imguring

class ImgurOauthHandler(BaseHandler):
    @authenticated
    def post(self):
        username = self.get_argument('username')
        password = self.get_argument('password')
        user = self.get_current_user()
        auth_token = imguring.get_xauth_token(username,password,i_consumer_key,i_consumer_secret)
        user['i_oauth_token'] = auth_token['oauth_token']
        user['i_oauth_token_secret'] = auth_token['oauth_token_secret']
        user['bind_imgur'] = True
        self.db.users.save(user)
        self.write('{"message":done}')

class ImgurUploadHandler(BaseHandler):
    def post(self):
        user = self.db.users.find_one({'password':self.get_argument('user')})
        #FUCK FUCK FUCK FUCK FUCK FUCKING FLASK
        api = imguring(i_consumer_key,i_consumer_secret,user['i_oauth_token'],user['i_oauth_token_secret'])
        for f in self.request.files['Filedata']:
            back = api.upload(f['body'])
            self.write(back['images']['links']['original'])

class ImgurCheckHandler(BaseHandler):
    def post(self):
        self.write('0')

class ImgurUnbindHandler(BaseHandler):
    @authenticated
    def get(self):
        user = self.get_current_user()
        del user['i_oauth_token'] ,user['i_oauth_token_secret'] ,user['bind_imgur']
        self.db.users.save(user)
        self.redirect('setting')

