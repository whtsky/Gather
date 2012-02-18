#coding=utf-8

import math
from common import BaseHandler,time_span
import time
import tornado.web

POST_PER_PAGE = 20

class TagCloudModule(tornado.web.UIModule):
    def render(self, db,limit=False):
        tags = sorted([ _ for _ in db.tags.find({'count':{'$gt':0}},{'_id':0})], key=lambda x: x['count'])
        tags.reverse()
        if limit!=False:
            tags = tags[:limit]
        html = []
        for tag in tags:
            html.append('<a href="/tag/%s" style="font-size:%spt;">%s</a>' % (tag['name'],round(math.log(tag['count'],tags[0]['count']+1))*14+8,tag['name']))
        return ' '.join(html)

class TagViewHandler(BaseHandler):
    def get(self,tagname):
        posts = self.db.posts.find({'tags':tagname},sort=[('changedtime', -1)])
        if posts:
            try:
                self.render('tag.html',tagname=tagname,posts=posts,
                    limit=POST_PER_PAGE,time_span=time_span,p=int(self.get_argument('p')))
            except:
                self.render('tag.html',tagname=tagname,posts=posts,
                    limit=POST_PER_PAGE,time_span=time_span,p=1)
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