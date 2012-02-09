#coding=utf-8

from common import BaseHandler
from hashlib import sha1,md5
from tornado.escape import json_encode

def hashpassword(username,password):
    password = md5(password).hexdigest()
    return sha1(username+password+username+password[1]).hexdigest()

class AuthSignupHandler(BaseHandler):
    def get(self):
        self.render('signup.html')

    def post(self):
        password = self.get_argument('password')
        username = self.get_argument('username')
        email = self.get_argument('email')
        account = self.db.users
        if len(username)>30 or len(password)>30:
            return
        elif account.find_one({'username':username})!=None or account.find_one({'email':email})!=None:
            message = '用户名或邮箱地址重复'
            status = 'error'
        else:
            account.insert({'_id':account.count(),
                        'username':username,
                        'email':email,
                        'password':hashpassword(username,password)})
            message = '注册成功'
            status = 'success'
        self.write(json_encode({'status':status,'message':message}))
        self.set_secure_cookie('user',username)

class AuthLogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie('user')
        self.redirect(self.get_argument('next', '/'))
        
class AuthLoginHandler(BaseHandler):
    def get(self):
        self.render('login.html')
        
    def post(self):
        username = self.get_argument('username')
        password = self.get_argument('password')
        account = self.db.users
        if account.find_one({'username':username,'password':hashpassword(username,password)})!=None:
            self.set_secure_cookie('user',username)
            self.write(json_encode({'status':'success','message':'登录成功'}))
        else:
            self.write(json_encode({'status':'error','message':'用户名或密码错误'}))
