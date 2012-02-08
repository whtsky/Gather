#coding=utf-8
import new

from common import BaseHandler
import tornado.web
from time import time
from common import time_span
from tornado.escape import json_encode

class PostHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        try:
            self.render('post.html',db=self.db,node=int(self.get_argument('node')))
        except:
            self.render('post.html',db=self.db,node=None)

    @tornado.web.authenticated
    def post(self):
        posts = self.db.posts
        posts.insert({'_id':posts.find_and_modify(update={'$inc':{'post_id':1}}, new=True)['post_id'],
                      'title':self.get_argument('title'),
                      'author':self.get_secure_cookie('user'),
                      'content':self.get_argument('html'),
                      'md':self.get_argument('markdown'),
                      'node':int(self.get_argument('nodeid')),
                      'comments':[],
                      'posttime':int(time()),
                      'tags':self.get_argument('tags').split(','),
                      })

class PostViewHandler(BaseHandler):
    def get(self,postid):
        self.render('postview.html',db=self.db,time_span=time_span,post=self.db.posts.find_one({'_id':int(postid)}))

    def post(self,postid):
        '''使用AJAX获取评论。返回JSON数据。
        每次返回10条数据。
        需要向本页面POST`start_num`数据。本数据为所需的第一条评论标号。
        比如，若需要取得第1-10条评论，则start_num为1.
        若无评论可获取则返回{}。
        '''
        start=int(self.get_argument('start_num'))
        comments=self.db.posts.find_one({'_id':int(postid)})['comments']
        count = comments.count()
        if start>count:
            self.write('{}')
        elif start+9>count:
            self.write(json_encode(zip(range(1,11),comments[start-1:count])))
        else:
            self.write(json_encode(zip(range(1,11),comments[start-1:start+9])))
