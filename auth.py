#coding=utf-8

from common import BaseHandler,time_span,html_killer
from hashlib import sha1,md5
from tornado.escape import json_encode, xhtml_escape, xhtml_unescape
import tornado.web
from tornado.web import authenticated
import time
from re import compile
from urlparse import urlparse

username_check = compile(u'(\w{1,25})')

def hashpassword(username,password):
    password = md5(password).hexdigest()
    return sha1(username+password).hexdigest()

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
        assert username_check.findall(username)[0]==username
        if account.find_one({'username_lower':username.lower()}) or account.find_one({'email':email}):
            message = '用户名或邮箱地址重复'
            status = 'error'
        else:
            account.insert({'_id':self.db.settings.find_and_modify(update={'$inc':{'user_id':1}}, new=True)['user_id'],
                        'username':username,
                        'username_lower':username.lower(),
                        'email':email,
                        'hashed_email':md5(email).hexdigest(),
                        'password':password,
                        'postmark':[],
                        'notification':[],
                        'block_user':[],
                        'twitter_bind':False,
                        'css':'',
                        'signtime':int(time.time())})
            message = '注册成功'
            status = 'success'
            self.set_secure_cookie('user',password)
        self.write(json_encode({'status':status,'message':message}))

class AuthLogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie('user')
        self.redirect(self.get_argument('next', '/'))
        
class AuthLoginHandler(BaseHandler):
    def get(self):
        if self.get_current_user():
            self.redirect(self.get_argument('next', '/'))
        else:
            self.render('login.html')
        
    def post(self):
        assert not self.get_current_user()
        username = self.get_argument('username')
        password = self.get_argument('password')
        password = hashpassword(username,password)
        if self.db.users.find_one({'username_lower':username.lower(),'password':password}):
            self.set_secure_cookie('user',password)
            self.write(json_encode({'status':'success','message':'登录成功'}))
        else:
            self.write(json_encode({'status':'error','message':'用户名或密码错误'}))

class AuthInfoHandler(BaseHandler):
    def get(self,username):
        user = self.db.users.find_one({'username_lower':username.lower()})
        if user:
            posts = self.db.posts.find({'author':username},sort=[('changedtime', -1)])
            comments = self.db.posts.find({'comments.author':username},sort=[('changedtime', -1)])
            self.render('authinfo.html',username=username,time_span=time_span,posts=posts,
                        comments=comments,user=user)
        else:
            raise tornado.web.HTTPError(404)

class AuthSettingHandler(BaseHandler):
    @authenticated
    def get(self):
        self.render('authsetting.html',user=self.get_current_user())

    @authenticated
    def post(self):
        user = self.get_current_user()
        for x in ('email','location','twitter','github','css'):
            user[x] = xhtml_unescape(self.get_argument(x,''))
            for x in set(html_killer.findall(user[x])):
                user[x] = user[x].replace(x,'')
        website = self.get_argument('website','')
        w = urlparse(website)
        if w[0] and w[1]:
            user['website'] = website
        else:
            user['website'] = ''
        self.db.users.save(user)
        self.redirect('/user/%s' % user['username'] )

class AuthChangePasswordHandler(BaseHandler):

    @authenticated
    def post(self):
        user = self.get_current_user()
        if user['password'] == hashpassword(username,self.get_argument('old')):
            user['password'] = hashpassword(username,self.get_argument('new'))
            self.db.users.save(user)
            self.write(json_encode({'status':'success','message':'修改密码成功'}))
        else:
            self.write(json_encode({'status':'fail','message':'原密码错误'}))

class BlockUserHandler(BaseHandler):
    @authenticated
    def get(self,username):
        user = self.get_current_user()
        if username in user['block_user']:
            user['block_user'].remove(username)
        else:
            user['block_user'].append(username)
        self.db.users.save(user)
        self.redirect('/user/'+username)

class NotificationHandler(BaseHandler):
    @authenticated
    def get(self):
        self.render('notifications.html',time_span=time_span)

    def post(self):
        u = self.get_current_user()
        u['notification'] = []
        self.db.users.save(u)
        self.redirect(self.get_argument('next', '/'))