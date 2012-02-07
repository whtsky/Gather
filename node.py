#coding=utf-8

from common import BaseHandler
POST_PER_PAGE = 20

class NodeViewHandler(BaseHandler):
    def get(self,nodeid):
        node=self.db.nodes.find_one({'_id':int(nodeid)})
        self.render('node.html',node=node,db=self.db,limit=POST_PER_PAGE)

    def post(self,nodeid):
        lastid = self.get_argument('lastid')