#coding=utf-8

import math
from common import BaseHandler,time_span
from hashlib import md5
import time

POST_PER_PAGE = 20

def tagcloud(db,limit=False):
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
        try:
            self.render('tag.html',tagname=tagname,posts=self.db.posts.find({'tags':tagname},sort=[('changedtime', -1)]),
                db=self.db,limit=POST_PER_PAGE,md5=md5,time_span=time_span,p=int(self.get_argument('p')))
        except:
            self.render('tag.html',tagname=tagname,posts=self.db.posts.find({'tags':tagname},sort=[('changedtime', -1)]),
                db=self.db,limit=POST_PER_PAGE,md5=md5,time_span=time_span,p=1)

class TagCloudHandler(BaseHandler):
    def get(self):
        self.render('tagcloud.html',tagcloud=tagcloud(self.db))

class TagFeedHandler(BaseHandler):
    def get(self,tagname):
        self.render('atom.xml',tagname=tagname,
                    time=time,posts=self.db.posts.find({'tags':tagname},sort=[('changedtime', 1)]))