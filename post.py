#coding=utf-8

from common import BaseHandler,time_span,md_convert
import tornado.web
from time import time
from tornado.escape import json_encode,xhtml_escape
from config import admin
from tag import POST_PER_PAGE

class PostHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        self.render('post.html')

    @tornado.web.authenticated
    def post(self):
        title = xhtml_escape(self.get_argument('title'))
        assert len(title)<26
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
                      'author':self.get_current_user()['username'],
                      'content':md_convert(md),
                      'comments':[],
                      'posttime':int(time()),
                      'changedtime':int(time()),
                      'tags':tags,
                      })
        for tag in tags:
            self.db.tags.update({'name':tag},
                                {'$inc':{'count':1}},
                                True)
        self.redirect('/topics/'+str(tid))

class PostViewHandler(BaseHandler):
    def get(self,postid):
        post = self.db.posts.find_one({'_id':int(postid)})
        if post:
            likelylist = {}
            for tag in post['tags']:
                for p in self.db.posts.find({'tags':tag}):
                    likelylist[p['_id']] =  likelylist.setdefault(p['_id'],1) + 1
            del likelylist[post['_id']]
            likelys = sorted(likelylist.items(),key=lambda x: x[1])
            likelyposts = [self.db.posts.find_one({'_id':x[0]}) for x in likelys]
            del likelys,likelylist
            comments = post['comments']
            for i in range(len(comments)):
                comments[i]['location'] =  str(i+1)
            self.render('postview.html',time_span=time_span,
                        post=post,admin_list=admin,comments=comments,likely=likelyposts)
        else:
            raise tornado.web.HTTPError(404)

    @tornado.web.authenticated
    def post(self,postid):
        md = self.get_argument('markdown')
        self.db.posts.update({'_id':int(postid)},
                {'$push':
                         {'comments':
                                  {'author':self.get_current_user()['username'],
                                   'content':md_convert(md),
                                   'posttime':int(time()),}},
                 '$set':{'changedtime':int(time())},})
        self.redirect('/topics/'+str(postid))

class MarkDownPreViewHandler(BaseHandler):
    def post(self):
        self.write(md_convert(self.get_argument('md')))

class TopicsViewHandler(BaseHandler):
    def get(self):
        try:
            self.render('topics.html',posts=self.db.posts.find({},sort=[('changedtime', -1)]),
                limit=POST_PER_PAGE,time_span=time_span,p=int(self.get_argument('p')))
        except:
            self.render('topics.html',posts=self.db.posts.find({},sort=[('changedtime', -1)]),
                limit=POST_PER_PAGE,time_span=time_span,p=1)

class PostListModule(tornado.web.UIModule):
    def render(self, db,posts):
        return self.render_string("modules/postlist.html", db=db,posts=posts,time_span=time_span,admin_list=admin)

class MarkPostHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self,postid):
        post = int(postid)
        username = self.get_current_user()['username']
        user = self.db.users.find_one({'username':username})
        if post in user['postmark']:
            self.db.users.update({'username':username},{'$pull':{'postmark':post}})
        else:
            self.db.users.update({'username':username},
                    {'$addToSet':{'postmark':post}})
        self.write('done.')

class MyMarkedPostHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render('markedpost.html')