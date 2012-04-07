#coding=utf-8

from tornado.web import authenticated
from tornado.escape import json_encode
from common import BaseHandler
from config import i_consumer_key,i_consumer_secret
from imguring import imguring

class ImgurOauthHandler(BaseHandler):
    @authenticated
    def post(self):
        username = self.get_argument('username')
        password = self.get_argument('password')
        user = self.current_user
        auth_token = imguring.get_xauth_token(username,password,i_consumer_key,i_consumer_secret)
        user['i_oauth_token'] = auth_token['oauth_token']
        user['i_oauth_token_secret'] = auth_token['oauth_token_secret']
        user['bind_imgur'] = True
        self.db.users.save(user)
        self.write('{"message":done}')

class ImgurUploadHandler(BaseHandler):
    def post(self):
        user = self.current_user
        if 'bind_imgur' not in user or not user['bind_imgur']:
            self.write(json_encode({'stat':'fail','msg':'你需要在个人设置页面中绑定imgur账号才可以上传图片'}))
            return
        api = imguring(i_consumer_key,i_consumer_secret,user['i_oauth_token'],user['i_oauth_token_secret'])
        back = api.upload(self.request.files['image'][0]['body'])
        self.write(json_encode({'stat':'success','url':back['images']['links']['original']}))

class ImgurUnbindHandler(BaseHandler):
    @authenticated
    def get(self):
        user = self.current_user
        del user['i_oauth_token'] ,user['i_oauth_token_secret'] ,user['bind_imgur']
        self.db.users.save(user)
        self.redirect('/setting')