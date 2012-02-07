#coding=utf-8

from common import BaseHandler
from hashlib import sha1
from tornado.escape import json_encode

def hashpassword(username,password):
    return sha1(username+password+username+password[1]+username[2]).hexdigest()

class AuthSignupHandler(BaseHandler):
    def get(self):
        self.render('signup.html')

    def post(self):
        password = self.get_argument('password')
        username = self.get_argument('username')
        email = self.get_argument('email')
        account = self.db.users
        if len(username)>30 or len(password)>30:
            message = 'username or password too lang'
        elif account.find_one({'username':username})!=None or account.find_one({'email':email})!=None:
            message = 'username or email already exist'
        elif:
            account.insert({'_id':account.count(),
                        'username':username,
                        'email':email,
                        'password':hashpassword(username,password)})
            message = 'success'
        self.write(json_encode({'message':message}))
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
            self.write(json_encode({'message':'success'}))
        else:
            self.write(json_encode({'message':'failed'}))
