#coding=utf-8

import tornado.web

class BaseHandler(tornado.web.RequestHandler):

    def __init__(self,*args,**kwargs):
        tornado.web.RequestHandler.__init__(self,*args,**kwargs)
        #方便调用
        self.db = self.application.db

    def get_current_user(self):
        return self.get_secure_cookie('user')

