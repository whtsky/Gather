#coding=utf-8

from common import BaseHandler
from hashlib import md5
POST_PER_PAGE = 20
from common import time_span
from tag import tagcloud

POST_PER_PAGE=15

class NodeViewHandler(BaseHandler):
    def get(self,nodeid):
        node=self.db.nodes.find_one({'_id':int(nodeid)})
        try:
            self.render('node.html',node=node,posts=self.db.posts.find({'node':node['_id']},sort=[('changedtime', 1)]),
                         db=self.db,limit=POST_PER_PAGE,md5=md5,time_span=time_span,tagcloud=tagcloud(self.db,limit=10),p=int(self.get_argument('p')))
        except:
            self.render('node.html',node=node,posts=self.db.posts.find({'node':node['_id']},sort=[('changedtime', 1)]),
                        db=self.db,limit=POST_PER_PAGE,md5=md5,tagcloud=tagcloud(self.db,limit=10),time_span=time_span,p=1)

    def post(self,nodeid):
        lastid = self.get_argument('lastid')
