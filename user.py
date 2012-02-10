#coding=utf-8

from common import BaseHandler,getvalue
from tornado.web import authenticated

class UserInfoHandler(BaseHandler):
    def get(self,username):
        self.render('userinfo.html',db=self.db,username=username)

class UserSettingHandler(BaseHandler):
    @authenticated
    def get(self):
        self.render('usersetting.html',user=self.db.find_one({'username':self.get_secure_cookie('user')}),
                    getvalue=getvalue)

    @authenticated
    def post(self):
        pass