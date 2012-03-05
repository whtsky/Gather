#coding=utf-8

from common import BaseHandler,time_span,md_convert
import tornado.web
from time import time
from tornado.escape import json_encode,xhtml_escape
from config import admin
from tag import POST_PER_PAGE
import twitter_oauth
from tornado.httpclient import AsyncHTTPClient
from common import html_killer,username_finder

class PostHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        self.render('post.html')

    def post(self):
        title = xhtml_escape(self.get_argument('title'))
        assert len(title)<51
        user = self.get_current_user()
        md = self.get_argument('markdown')
        posts = self.db.posts
        tid = self.db.settings.find_and_modify(update={'$inc':{'post_id':1}}, new=True)['post_id']
        tags = []
        for x in xhtml_escape(self.get_argument('tags').lower()).split(','):
            for x in x.split(' '):
                for x in x.split('/'):
                    tags.append(x)
        time_now = int(time())
        posts.insert({'_id':tid,
                      'title':title,
                      'author':user['username'],
                      'content':md_convert(md,notice=True,time=time_now,user=user['username'],db=self.db,postid=tid),
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
        if user['twitter_bind'] and user['twitter-sync']:
            self.title = title
            self.user = user
            http_client = AsyncHTTPClient()
            http_client.fetch('http://is.gd/create.php?format=simple&url=%s/topics/%s' % (self.application.settings['bbs_url'],tid), self.sync)

    def sync(self,request):
        api = twitter_oauth.Api(self.application.consumer_key,self.application.consumer_secret, self.user['oauth_token'], self.user['oauth_token_secret'])
        api.post_update(tweet=u'%s : %s' % (self.title,request.body))

class PostViewHandler(BaseHandler):
    def get(self,postid):
        postid = int(postid)
        post = self.db.posts.find_one({'_id':postid})
        user = self.get_current_user()
        if user:
            change = False
            for m in user['notification']:
                if m['postid'] == postid and m['read'] == False:
                    m['read'] = True
                    change = True
            self.db.users.save(user)
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

    def post(self,postid):
        md = self.get_argument('markdown')
        time_now = int(time())
        user = self.get_current_user()
        postid = int(postid)
        content = md_convert(md,notice=True,time=time_now,user=user,db=self.db,postid=postid)
        self.db.posts.update({'_id':postid},
                {'$push':
                         {'comments':
                                  {'author':user['username'],
                                   'content':content,
                                   'posttime':int(time()),
                                   }
                         },
                 '$set':{'changedtime':int(time())},})
        self.redirect('/topics/'+str(postid))

        if user['twitter_bind'] and user['twitter-sync']:
            self.content = content
            self.user = user
            http_client = AsyncHTTPClient()
            http_client.fetch('http://is.gd/create.php?format=simple&url=%s/topics/%s' % (self.application.settings['bbs_url'],postid), self.sync)

    def sync(self,request):
        for i in set(html_killer.findall(self.content)):
            self.content = self.content.replace(i,'')#不知道为什么，直接用sub返回的是空字符串。
        for i in set(username_finder.findall(self.content)):
            user = self.db.users.find_one({'username':i})
            if user and 'twitter' in user:
                self.content = self.content.replace(u'@'+i,u'@'+user['twitter'])
            else:
                self.content = self.content.replace(u'@'+i,'')
        api = twitter_oauth.Api(self.application.consumer_key,self.application.consumer_secret, self.user['oauth_token'], self.user['oauth_token_secret'])
        api.post_update(tweet=u'%s : %s' % (self.content[:100],request.body))

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