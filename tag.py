#coding=utf-8

import math
from common import BaseHandler,time_span
import time
import tornado.web

class TagCloudModule(tornado.web.UIModule):
    def render(self, db, mc, limit=False):
        try:
            html = mc['tagcloud:%s' % limit]
        except KeyError:
            tags = db.tags.find({'count':{'$gt':0}},{'_id':0},sort=[('count', -1)],limit=limit)
            html = []
            for tag in tags:
                html.append(u'<a href="/tag/%s" style="font-size:%spt;" title="共%s条主题">%s</a>' % (tag['name'],int(3 * math.log(max(tag['count'] + 1, 1))) + 12,tag['count'],tag['name']))
            html =  ' '.join(html)
            mc.set('tagcloud:%s' % limit,html,time=18000)
        return html

class TagViewHandler(BaseHandler):
    def get(self,tagname):
        posts = self.db.posts.find({'tags':tagname.lower()},sort=[('changedtime', -1)])
        if not posts.count():
            raise tornado.web.HTTPError(404)
        p = int(self.get_argument('p',1))
        tag_sidebar = self.db.tags.find_one({'name':tagname})
        tag_sidebar = 'sidebar' in tag_sidebar and tag_sidebar['sidebar'] or ''
        self.render('tag.html',tagname=tagname,posts=posts,
            time_span=time_span,p=p,tag_sidebar=tag_sidebar)

    def post(self,tagname):
        self.db.tags.update({'name':tagname},{'$set':{'sidebar':self.get_argument('sidebar','')}})
        self.redirect('/tag/%s' % tagname)

class TagCloudHandler(BaseHandler):
    def get(self):
        self.render('tagcloud.html')

class TagFeedHandler(BaseHandler):
    def get(self,tagname):
        self.set_header("Content-Type", "application/atom+xml")
        url = '/tag/'+tagname
        posts = [_ for _ in self.db.posts.find({'tags':tagname},sort=[('changedtime', 1)],limit=20)]
        tornado.web.RequestHandler.render(self,'atom.xml',url=url,name=tagname,
                    time=time,posts=posts)
