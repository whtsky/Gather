#coding=utf-8

from common import BaseHandler
import tornado.web

class AdminAddNodeHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self,nodename):
        if self.get_secure_cookie('user') not in ('jybox','whtsky'):
            return 
        nodes = self.db.nodes
        nodes.insert({'_id':self.db.settings.find_and_modify(update={'$inc':{'node_id':1}}, new=True)['node_id'],
                      'name':nodename,
                      })