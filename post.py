#coding=utf-8
import new

from common import BaseHandler,time_span
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
        posts = self.db.posts
        tid = self.db.settings.find_and_modify(update={'$inc':{'post_id':1}}, new=True)['post_id']
        tags = []
        for x in self.get_argument('tags').split(','):
            for x in x.split(' '):
                for x in x.split('/'):
                    tags.append(x)
        posts.insert({'_id':tid,
                      'title':xhtml_escape(self.get_argument('title')),
                      'author':self.get_secure_cookie('user'),
                      'content':xhtml_escape(self.get_argument('html')),
                      'md':self.get_argument('markdown'),
                      'node':int(self.get_argument('nodeid')),
                      'comments':[],
                      'posttime':int(time()),
                      'tags':tags,
                      })
        message = '发表成功'
        status = 'success'
        self.write(json_encode({'status':status,'message':message,'tid':tid}))
        self.db.settings.update({'name':'tag-count'},{'$inc':dict(zip(tags,[1]*len(tags)))})

class CommentHandler(BaseHandler):

    @tornado.web.authenticated
    def post(self,postid):
        self.db.posts.update({'_id':postid},
                             {'$push':
                             {'comments':
                             {'author':self.get_secure_cookie('user'),
                              'content':xhtml_escape(self.get_argument('html')),
                              'md':self.get_argument('markdown'),
                              'posttime':int(time()),
                             }
                             }
                             }
                            )

class PostViewHandler(BaseHandler):
    def get(self,postid):
        self.render('postview.html',db=self.db,time_span=time_span,
                    post=self.db.posts.find_one({'_id':int(postid)}),md5=md5)

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
            return
        elif start+9>count:
            comments = comments[start-1:count]
        else:
            comments = comments[start-1:start+9]
        for i in comments:
            i['posttime'] = time_span(i['posttime'])
            i['author_email'] = self.db.users.find_one({"username":i["author"]})["email"]
        self.write(json_encode(zip(range(1,len(comments)+1),comments)))