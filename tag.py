#coding=utf-8

import math
from node import POST_PER_PAGE
from common import BaseHandler,time_span
from hashlib import md5
import time

def tagcloud(db,limit=100):
    tags =  [_ for _ in reversed(sorted(db.settings.find_one({'name':'tag-count'},{'_id':0,'name':0}).items(), key=lambda x: x[1])[:limit])]
    return ''.join(['<a href="/tag/%s" style="font-size:%spt;">%s</a>' % (x,round(math.log(y,tags[0][1]),1)*14+8,x)) for x,y in tags])
class TagViewHandler(BaseHandler):
    def get(self,tagname):
        try:
            self.render('tag.html',tagname=tagname,posts=self.db.posts.find({'tags':tagname},sort=[('changedtime', 1)]),
                db=self.db,limit=POST_PER_PAGE,md5=md5,time_span=time_span,p=int(self.get_argument('p')))
        except:
            self.render('tag.html',tagname=tagname,posts=self.db.posts.find({'tags':tagname},sort=[('changedtime', 1)]),
                db=self.db,limit=POST_PER_PAGE,md5=md5,time_span=time_span,p=1)

class TagCloudHandler(BaseHandler):
    def get(self):
        self.render('tagcloud.html',tagcloud=tagcloud(self.db))

class TagFeedHandler(BaseHandler):
    def get(self,tagname):
        self.render('atom.xml',tagname=tagname,
                    time=time,posts=self.db.posts.find({'tags':tagname},sort=[('changedtime', 1)]))