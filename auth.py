#coding=utf-8

from common import BaseHandler,getvalue,time_span
from hashlib import sha1,md5
from tornado.escape import json_encode
from tornado.web import authenticated

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
            self.set_secure_cookie('user',username)
        self.write(json_encode({'status':status,'message':message}))

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

class AuthInfoHandler(BaseHandler):
    def get(self,username):
        posts = self.db.posts.find({'author':username},sort=[('changedtime', -1)])
        comments = self.db.posts.find({'comments.author':username},sort=[('changedtime', -1)])
        self.render('authinfo.html',username=username,time_span=time_span,md5=md5,posts=posts,
                    comments=comments,user=self.db.users.find_one({'username':username}))

class AuthSettingHandler(BaseHandler):
    @authenticated
    def get(self):
        self.render('authsetting.html',user=self.db.users.find_one({'username':self.get_secure_cookie('user')}),
            getvalue=getvalue,md5=md5)

    @authenticated
    def post(self):
        setting = {}
        for x in ('email','website','location','twitter','github'):
            setting[x] = self.get_argument(x)
        self.db.users.update({'name':self.get_secure_cookie('user')},{'$set':setting})
        self.write(json_encode({'status':'success'}))

class AuthChangePasswordHandler(BaseHandler):

    @authenticated
    def post(self):
        username = self.get_secure_cookie('user')
        if self.db.users.find_one({'username':username,'password':hashpassword(username,self.get_argument('old'))}) == None:
            self.write(json_encode({'status':'fail','message':'原密码错误'}))
        else:
            self.db.users.update({'username':username},{'$set':{'password':hashpassword(username,self.get_argument('new'))}})
            self.write(json_encode({'status':'success','message':'修改密码成功'}))