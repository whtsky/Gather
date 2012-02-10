#coding=utf-8

from common import BaseHandler

class UserInfoHandler(BaseHandler):
    def get(self,username):
        self.render('userinfo.html',db=self.db,username=username)