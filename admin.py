#coding=utf-8

from common import BaseHandler
import tornado.web

class AdminAddNodeHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self,nodename):
        if self.get_secure_cookie('user') not in ('jybox','whtsky'):
            return 
        nodes = self.db.nodes
        nodes.insert({'_id':nodes.count(),
                      'name':nodename,
                      })