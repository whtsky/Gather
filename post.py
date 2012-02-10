#coding=utf-8

from common import BaseHandler,time_span,md_convert
import tornado.web
from time import time
from tornado.escape import json_encode,xhtml_escape
from hashlib import md5

class PostHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        try:
            self.render('post.html',db=self.db,node=int(self.get_argument('node')))
        except:
            self.render('post.html',db=self.db,node=None)

    @tornado.web.authenticated
    def post(self):
        title = xhtml_escape(self.get_argument('title'))
        assert len(title)<50
        md = self.get_argument('markdown')
        posts = self.db.posts
        tid = self.db.settings.find_and_modify(update={'$inc':{'post_id':1}}, new=True)['post_id']
        tags = []
        for x in self.get_argument('tags').split(','):
            for x in x.split(' '):
                for x in x.split('/'):
                    tags.append(xhtml_escape(x))
        posts.insert({'_id':tid,
                      'title':title,
                      'author':self.get_secure_cookie('user'),
                      'content':md_convert(xhtml_escape(md)),
                      'md':md,
                      'node':int(self.get_argument('nodeid')),
                      'comments':[],
                      'posttime':int(time()),
                      'changedtime':int(time()),
                      'tags':tags,
                      })
        message = '发表成功'
        status = 'success'
        self.write(json_encode({'status':status,'message':message,'tid':tid}))
        for tag in tags:
            self.db.tags.update({'name':tag},
                                {'$inc':{'count':1}},
                                True)

class CommentHandler(BaseHandler):

    @tornado.web.authenticated
    def post(self,postid):
        md = self.get_argument('markdown')
        self.db.posts.update({'_id':int(postid)},
                             {'$push':
                             {'comments':
                             {'author':self.get_secure_cookie('user'),
                              'content':xhtml_escape(md_convert(md)),
                              'md':md,
                              'posttime':int(time()),}},
                              '$set':{'changedtime':int(time())},})
        message = '发表成功'
        status = 'success'
        self.write(json_encode({'status':status,'message':message}))

class PostViewHandler(BaseHandler):
    def get(self,postid):
        self.render('postview.html',db=self.db,time_span=time_span,
                    post=self.db.posts.find_one({'_id':int(postid)}),md5=md5)

    def post(self,postid):
        start=int(self.get_argument('start_num'))
        comments=self.db.posts.find_one({'_id':int(postid)},{'comments':{'$slice':[start-1,10]}})['comments']
        self.render('comments.html',comments=comments,md5=md5,time_span=time_span,db=self.db)

class MarkDownPreViewHandler(BaseHandler):
    def post(self):
        self.write(md_convert(xhtml_escape(self.get_argument('md'))))
