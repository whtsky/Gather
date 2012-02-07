#coding=utf-8

from common import BaseHandler
import tornado.web
from time import time

class PostHandler(BaseHandler):

#    @tornado.web.authenticated
    def get(self):
        try:
            self.render('post.html',db=self.db,node=int(self.get_argument('node')))
        except:
            self.render('post.html',db=self.db,node=None)


#    @tornado.web.authenticated
    def post(self):
        posts = self.db.posts
        posts.insert({'_id':posts.find_and_modify(update={'$inc':{'post_id':1}}, new=True).get('post_id'),
                      'title':self.get_argument('title'),
                      'author':self.get_secure_cookie('user'),
                      'content':self.get_argument('markdown'),
                      'node':int(self.get_argument('nodeid')),
                      'comments':[],
                      'posttime':int(time()),
                      'changedtime':int(time()),#发表评论请更新此条
                      'tags':self.get_argument('tags').split(','),
                      })
