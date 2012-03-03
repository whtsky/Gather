#coding=utf-8

from common import BaseHandler,getvalue,time_span
from hashlib import sha1,md5
from tornado.escape import json_encode
import tornado.web
from tornado.web import authenticated
from config import admin
import time
from re import compile

username_check = compile(u'([\u4e00-\u9fa5A-Za-z0-9]+)')

def hashpassword(username,password):
    password = md5(password).hexdigest()
    return sha1(username.encode('utf-8')+password).hexdigest()

class AuthSignupHandler(BaseHandler):
    def get(self):
        if self.get_current_user():
            self.redirect(self.get_argument('next', '/'))
        self.render('signup.html')

    def post(self):
        assert not self.get_current_user()
        password = self.get_argument('password')
        username = self.get_argument('username')
        email = self.get_argument('email')
        account = self.db.users
        password = hashpassword(username,password)
        assert len(username)<16
        #assert username_check.findall(username)[0]==username
        if account.find_one({'username':username}) or account.find_one({'email':email}):
            message = '用户名或邮箱地址重复'
            status = 'error'
        else:
            account.insert({'_id':self.db.settings.find_and_modify(update={'$inc':{'user_id':1}}, new=True)['user_id'],
                        'username':username,
                        'email':email,
                        'hashed_email':md5(email).hexdigest(),
                        'password':password,
                        'tagmark':[],
                        'postmark':[],
                        'notification':[],
                        'twitter_bind':False,
                        'signtime':int(time.time())})
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
        if self.get_current_user():
            self.redirect(self.get_argument('next', '/'))
        self.render('login.html')
        
    def post(self):
        assert not self.get_current_user()
        username = self.get_argument('username')
        password = self.get_argument('password')
        account = self.db.users
        if account.find_one({'username':username,'password':hashpassword(username,password)}):
            self.set_secure_cookie('user',username)
            self.write(json_encode({'status':'success','message':'登录成功'}))
        else:
            self.write(json_encode({'status':'error','message':'用户名或密码错误'}))

class AuthInfoHandler(BaseHandler):
    def get(self,username):
        user = self.db.users.find_one({'username':username})
        if user:
            posts = self.db.posts.find({'author':username},sort=[('changedtime', -1)])
            comments = self.db.posts.find({'comments.author':username},sort=[('changedtime', -1)])
            self.render('authinfo.html',username=username,time_span=time_span,posts=posts,
                        comments=comments,user=user,admin_list=admin)
        else:
            raise tornado.web.HTTPError(404)

class AuthSettingHandler(BaseHandler):
    @authenticated
    def get(self):
        self.render('authsetting.html',user=self.db.users.find_one({'username':self.get_current_user()['username']}),
            getvalue=getvalue)

    @authenticated
    def post(self):
        setting = {}
        for x in ('email','website','location','twitter','github'):
            try:
              setting[x] = self.get_argument(x)
            except:
                pass
        setting['twitter-sync'] = self.get_argument('twitter_sync') == 'true'
        if self.db.users.find_one({'username':{'$ne':self.get_current_user()['username']},'email':setting['email']}):
            self.write(json_encode({'status':'fail','message':'邮箱已有人使用。'}))
            return
        setting['hashed_email'] = md5(setting['email']).hexdigest()
        self.db.users.update({'username':self.get_current_user()['username']},{'$set':setting})
        self.write(json_encode({'status':'success','message':'信息更新成功'}))

class AuthChangePasswordHandler(BaseHandler):

    @authenticated
    def post(self):
        username = self.get_current_user()['username']
        if self.db.users.find_one({'username':username,'password':hashpassword(username,self.get_argument('old'))}):
            self.db.users.update({'username':username},{'$set':{'password':hashpassword(username,self.get_argument('new'))}})
            self.write(json_encode({'status':'success','message':'修改密码成功'}))
        else:
            self.write(json_encode({'status':'fail','message':'原密码错误'}))

class NotificationHandler(BaseHandler):
    @authenticated
    def get(self):
        self.render('notifications.html',time_span=time_span)

    def post(self):
        u = self.get_current_user()
        u['notification'] = []
        self.db.users.save(u)
        self.redirect(self.get_argument('next', '/'))