#coding=utf-8

import tornado.web
from time import time

class BaseHandler(tornado.web.RequestHandler):

    def __init__(self,*args,**kwargs):
        tornado.web.RequestHandler.__init__(self,*args,**kwargs)
        #方便调用
        self.db = self.application.db

    def get_current_user(self):
        return self.get_secure_cookie('user')

def time_span(t):
    timecha = int(time()) - t
    if timecha < 60:
        return str(timecha)+u'秒前'
    elif timecha < 3600:
        return str(timecha/60)+u'分钟前'
    elif timecha < 86400:
        return str(timecha/3600)+u'小时前'
    elif timecha < 2678400:
        return str(timecha/86400)+u'天前'
    elif timecha < 32140800:
        return str(timecha/2678400)+u'月前'
    else:
        return str(timecha/32140800)+u'年前'