#coding=utf-8

from common import BaseHandler
import tornado.web
from time import time

class PostHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self,nodeid):
        '''直接渲染模板
        '''
        pass


    @tornado.web.authenticated
    def post(self,nodename):
        posts = self.db.posts
        posts.insert({'_id':posts.find_and_modify(update={'$inc':{'post_id':1}}, new=True).get('post_id'),
                      'title':self.get_argument('title'),
                      'author':self.get_secure_cookie('user'),
                      'content':self.get_argument('content'),
                      'node':nodeid,
                      'comments':{},
                      'posttime':int(time()),
                      'tags':self.get_argument('tags').split(','),
                      })