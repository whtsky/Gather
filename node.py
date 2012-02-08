#coding=utf-8

from common import BaseHandler
from hashlib import md5
POST_PER_PAGE = 20
from time import time

class NodeViewHandler(BaseHandler):
    def get(self,nodeid):
        node=self.db.nodes.find_one({'_id':int(nodeid)})
        self.render('node.html',node=node,db=self.db,limit=POST_PER_PAGE,md5=md5,time_span=time_span)

    def post(self,nodeid):
        lastid = self.get_argument('lastid')

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