#coding=utf-8

from common import BaseHandler
from hashlib import sha1

def hashpassword(username,password):
    return sha1(username+password+username+password[1]+username[2]).hexdigest()

class AuthSignupHandler(BaseHandler):
    def get(self):
        self.render('signup.html')

    def post(self):
        password = self.get_argument('password')
        if password != self.get_argument('password-ag'):
            self.render('error.html',errortext='两次密码不一样。')
            return 
        username = self.get_argument('username')
        email = self.get_argument('email')
        account = self.db.users
        if account.find_one({'username':username})!=None or account.find_one({'email':email})!=None:
            self.render('error.html',errortext='用户名或邮箱已存在。')
            return 
        account.insert({'_id':account.count(),
                        'username':username,
                        'email':email,
                        'password':hashpassword(username,password)})
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
        if account.find_one({'username':username,'password':hashpassword(username,password)})!=None:
            self.set_secure_cookie('user',username)
            self.redirect('/')