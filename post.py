#coding=utf-8

from common import BaseHandler,time_span,md_convert
import tornado.web
from time import time
from tornado.escape import xhtml_escape
from config import POST_PER_PAGE
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
        for x in xhtml_escape(self.get_argument('tags').lower()).replace(',',' ').replace('/',' ').split(' '):
            if x:
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
        try:
            del self.mc['index']
        except KeyError:
            pass
        self.redirect('/topics/'+str(tid))
        if user['twitter_bind'] and self.get_argument('twitter-sync') == 'yes':
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
        user = self.get_current_user()
        if user:
            change = False
            for m in user['notification']:
                if m['postid'] == postid and m['read'] == False:
                    m['read'] = True
                    change = True
            if change:
                self.db.users.update({'username':user['username']},{'$set':{'notification':user['notification']}})
        try:
            cache = self.mc[str(postid)]
        except KeyError:
            cache = [0,1,2,3]

            cache[0] = post = self.db.posts.find_one({'_id':postid})

            cache[1] = authorposts = [ _ for _ in self.db.posts.find({'author':post["author"],'_id':{'$ne':postid}},sort=[('changedtime', -1)],limit=5)]

            likelylist = {}
            for tag in post['tags']:
                for p in self.db.posts.find({'tags':tag}):
                    likelylist[p['_id']] =  likelylist.setdefault(p['_id'],1) + 1
            del likelylist[post['_id']]
            likelys = sorted(likelylist.items(),key=lambda x: x[1])
            cache[2] = likelyposts = [self.db.posts.find_one({'_id':x[0]}) for x in likelys[:5]]

            for i in range(len(post['comments'])):
                post['comments'][i]['location'] =  str(i+1)

            cache[3] = comments = self.render_string('modules/comments.html',db=self.db,time_span=time_span,post=post)

            self.mc.set(str(postid),cache,time=43200)
        else:
            post = cache[0]
            authorposts = cache[1]
            likelyposts = cache[2]
            comments = cache[3]
        self.render('postview.html',time_span=time_span,comments=comments,
                    post=post,likely=likelyposts,authorposts=authorposts)

    def post(self,postid):
        md = self.get_argument('markdown')
        time_now = int(time())
        user = self.get_current_user()
        postid = int(postid)
        content = md_convert(md,notice=True,time=time_now,user=user['username'],db=self.db,postid=postid)
        post = self.db.posts.fine_one({'_id':postid})
        post['comments'].append({'author':user['username'],
                                 'content':content,
                                 'posttime':int(time()),
                                 })
        post['changedtime'] = int(time())
        self.db.posts.save(post)
        try:
            del self.mc['index']
        except KeyError:
            pass
        try:
            cache = self.mc[str(postid)]
        except KeyError:
            pass
        else:
            cache[3] = self.render_string('modules/comments.html',db=self.db,time_span=time_span,post=post)
            self.mc[str(postid)] = cache

        self.redirect('/topics/'+str(postid))

        if user['twitter_bind'] and self.get_argument('twitter-sync') == 'yes':
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
                self.content = self.content.replace(u'@'+i,u' @'+user['twitter'])
            else:
                self.content = self.content.replace(u'@'+i,i)
        api = twitter_oauth.Api(self.application.consumer_key,self.application.consumer_secret, self.user['oauth_token'], self.user['oauth_token_secret'])
        api.post_update(tweet=u'%s : %s' % (self.content[:100],request.body))

class MarkDownPreViewHandler(BaseHandler):
    def post(self):
        self.write(md_convert(self.get_argument('md')))

class TopicsViewHandler(BaseHandler):
    def get(self):
        try:
            p = int(self.get_argument('p'))
        except:
            p = 1
        self.render('topics.html',posts=self.db.posts.find({},sort=[('changedtime', -1)]),
            time_span=time_span,p=p)

class PostListModule(tornado.web.UIModule):
    def render(self, db, mc, posts,p=None,name=None):
        if name:
            try:
                p = mc[name]
            except KeyError:
                pass
            else:
                return p
        args = dict(db=db,mc=mc,posts=posts,time_span=time_span,p=p)
        if p:
            args['count'] = posts.count()
            args['posts'] = args['posts'].skip((p-1)*POST_PER_PAGE).limit(POST_PER_PAGE)
            args['limit'] = POST_PER_PAGE
        p = self.render_string("modules/postlist.html",**args)
        if name:
            mc[name] = p
        return p
class MarkPostHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self,postid):
        post = int(postid)
        user = self.get_current_user()
        if post in user['postmark']:
            user['postmark'].remove(post)
        else:
            user['postmark'].append(post)
        self.db.users.save(user)
        self.mc['user:%s' % user['username'].encode('utf-8')] = user
        self.write('done.')

class MyMarkedPostHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render('markedpost.html')