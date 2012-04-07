#coding=utf-8

from common import BaseHandler,time_span,md_convert
import tornado.web
from tornado.escape import xhtml_escape
from tornado.auth import TwitterMixin
from time import time
from config import POST_PER_PAGE
from common import html_killer,username_finder
from ping import ping

class PostHandler(BaseHandler, TwitterMixin):
    @tornado.web.authenticated
    def get(self):
        self.render('post.html')

    def post(self):
        title = xhtml_escape(self.get_argument('title'))
        assert len(title)<51
        user = self.current_user
        md = self.get_argument('markdown')
        posts = self.db.posts
        tags = []
        for x in xhtml_escape(self.get_argument('tags').lower()).split(' '):
            if x:
                tags.append(x)
        post = self.db.posts.find_one({'title':title,'author':user['username'],'tags':tags})
        if post:#Topic has already been posted.
            self.redirect('/topics/'+str(post['_id']))
            return
        time_now = int(time())
        tid = self.db.settings.find_and_modify(update={'$inc':{'post_id':1}}, new=True)['post_id']
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
            del self.mc['tagcloud:10']
            del self.mc['tagcloud:False']
        except KeyError:
            pass
        self.redirect('/topics/'+str(tid))
        url = '%s/topics/%s' % (self.application.settings['forum_url'],tid)
        if user['twitter_bind'] and self.get_argument('twitter-sync') == 'yes':
            self.twitter_request(
                '/statuses/update',
                post_args={'status': u'%s %s' % (title,url)},
                access_token=user['access_token'],callback=self._on_post)
        ping(self.application.settings['forum_title_e'],self.application.settings['forum_url'],url)

    def _on_post(self,entry):
        pass

class PostViewHandler(BaseHandler, TwitterMixin):
    def get(self,postid):
        postid = int(postid)
        user = self.current_user
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
            cache = [0,1,2]

            cache[0] = post = self.db.posts.find_one({'_id':postid})
            if not post:
                raise tornado.web.HTTPError(404)

            authorposts = self.db.posts.find({'author':post["author"],'_id':{'$ne':postid}},sort=[('changedtime', -1)],limit=5)

            likelylist = {}
            for tag in post['tags']:
                for p in self.db.posts.find({'tags':tag}):
                    likelylist[p['_id']] =  likelylist.setdefault(p['_id'],1) + 1
            del likelylist[post['_id']]
            likelys = sorted(likelylist.items(),key=lambda x: x[1])
            likelyposts = [self.db.posts.find_one({'_id':x[0]}) for x in likelys[:5]]

            cache[1] = sidebar = self.render_string('modules/postview-sidebar.html',likely=likelyposts,authorposts=authorposts)

            for i in range(len(post['comments'])):
                post['comments'][i]['location'] =  str(i+1)

            cache[2] = comments = self.render_string('modules/comments.html',db=self.db,time_span=time_span,post=post)

            self.mc.set(str(postid),cache,time=43200)
        else:
            post = cache[0]
            sidebar = cache[1]
            comments = cache[2]
        self.render('postview.html',time_span=time_span,comments=comments,
                    post=post,sidebar=sidebar)

    def post(self,postid):
        md = self.get_argument('markdown')
        time_now = int(time())
        user = self.current_user
        postid = int(postid)
        content = md_convert(md,notice=True,time=time_now,user=user['username'],db=self.db,postid=postid)
        post = self.db.posts.find_one({'_id':postid})
        source = self.parse_user_agent()

        comment_reversed = reversed(post['comments'])
        for _ in range(min(len(post['comments']),5)):#look up in the recently 5 comment
            comment = comment_reversed.next()
            if comment['author'] == user['username'] and comment['content'] == content:#Reply has already been posted.
                self.redirect('/topics/'+str(postid))
                return

        post['comments'].append({'author':user['username'],
                                 'content':content,
                                 'posttime':time_now,
                                 })
        post['changedtime'] = time_now
        if source:
            post['comments'][-1]['source'] = source
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
            for i in range(len(post['comments'])):
                post['comments'][i]['location'] =  str(i+1)
            cache[2] = self.render_string('modules/comments.html',db=self.db,time_span=time_span,post=post)
            self.mc[str(postid)] = cache

        self.redirect('/topics/'+str(postid))
        url = '%s/topics/%s#reply-%s' % (self.application.settings['forum_url'],postid,len(post['comments']))
        if user['twitter_bind'] and self.get_argument('twitter-sync') == 'yes':
            for i in set(html_killer.findall(content)):
                content = content.replace(i,'')#不知道为什么，直接用sub返回的是空字符串。
            for i in set(username_finder.findall(content)):
                u = self.db.users.find_one({'username':i})
                if u and 'twitter' in u:
                    content = content.replace(u'@'+i,u' @'+user['twitter'])
            self.twitter_request(
                '/statuses/update',
                post_args={'status': u'%s %s' % (content,url)},
                access_token=user['access_token'],callback=self._on_post)
        ping(self.application.settings['forum_title_e'],self.application.settings['forum_url'],url)

    def _on_post(self,entry):
        pass

class MarkDownPreViewHandler(BaseHandler):
    def post(self):
        self.write(md_convert(self.get_argument('md','')))

class TopicsViewHandler(BaseHandler):
    def get(self):
        p = int(self.get_argument('p',1))
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
        user = self.current_user
        if post in user['postmark']:
            user['postmark'].remove(post)
        else:
            user['postmark'].append(post)
        self.db.users.save(user)
        self.write('done.')

class MyMarkedPostHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render('markedpost.html')