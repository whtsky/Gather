#coding=utf-8

import math
from common import BaseHandler,time_span,getuser
import time
import tornado.web

POST_PER_PAGE = 20

class TagCloudModule(tornado.web.UIModule):
    def render(self, db, mc, limit=False):
        try:
            html = mc['tagcloud:%s' % limit]
        except KeyError:
            tags = [ tag for tag in db.tags.find({'count':{'$gt':0}},{'_id':0},sort=[('count', -1)],limit=limit)]
            html = []
            for tag in tags:
                html.append('<a href="/tag/%s" style="font-size:%spt;">%s</a>' % (tag['name'],round(math.log(tag['count'],tags[0]['count']))*14+8,tag['name']))
            html =  ' '.join(html)
            mc.set('tagcloud:%s' % limit,html,time=1800)
        return html

class TagViewHandler(BaseHandler):
    def get(self,tagname):
        posts = self.db.posts.find({'tags':tagname.lower()},sort=[('changedtime', -1)])
        if posts:
            try:
                p = int(self.get_argument('p'))
            except:
                p = 1
            self.render('tag.html',tagname=tagname,posts=posts,
                limit=POST_PER_PAGE,time_span=time_span,getuser=getuser,p=p)

        else:
            raise tornado.web.HTTPError(404)

class TagCloudHandler(BaseHandler):
    def get(self):
        self.render('tagcloud.html')

class TagFeedHandler(BaseHandler):
    def get(self,tagname):
        self.set_header("Content-Type", "application/atom+xml")
        url = '/tag/'+tagname
        tornado.web.RequestHandler.render(self,'atom.xml',url=url,name=tagname,
                    time=time,posts=self.db.posts.find({'tags':tagname},sort=[('changedtime', 1)]))
