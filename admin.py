#coding=utf-8
from tornado.escape import xhtml_escape

from common import BaseHandler,time_span
from config import admin

class RemoveUserHandler(BaseHandler):
    def get(self,username):
        assert self.get_current_user()['username'] in admin
        self.db.users.remove({'username':username})
        removepost(fliter={'author':username},db=self.db)
        postids = []
        for post in self.db.posts.find({'comments.author':username}):
            postids.append(post['_id'])
        self.db.posts.update({'comments.author':username},
                {'$pull':{'comments':{'author':username}}},multi=True)
        self.write('done.')
        try:
            del self.mc['index']
            for postid in postids:
                del self.mc[str(postid)]
        except KeyError:
            pass

class RemovePostHandler(BaseHandler):
    def get(self,postid):
        assert self.get_current_user()['username'] in admin
        postid = int(postid)
        removepost(fliter={'_id':postid},db=self.db)
        self.write('done.')
        try:
            del self.mc['index']
        except KeyError:
            pass

class RemoveCommentHandler(BaseHandler):
    def get(self,postid,commentid):
        assert self.get_current_user()['username'] in admin
        self.write(commentid)
        post = self.db.posts.find_one({'_id':int(postid)})
        del post['comments'][int(commentid)-1]
        self.db.posts.save(post)
        self.write('done.')
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

class ChangeTagHandler(BaseHandler):
    def post(self,postid):
        assert self.get_current_user()['username'] in admin
        postid = int(postid)
        for tag in self.db.posts.find_one({'_id':postid})['tags']:
            self.db.tags.update({'name':tag},{'$inc':{'count':-1}})
        tags = []
        for x in xhtml_escape(self.get_argument('tags').lower()).split(','):
            for x in x.split(' '):
                for x in x.split('/'):
                    tags.append(x)
        for tag in tags:
            self.db.tags.update({'name':tag},
                        {'$inc':{'count':1}},True)
        self.db.posts.update({'_id':postid},{'$set':{'tags':tags}})
        self.write('done.')
        try:
            del self.mc['index']
            del self.mc[str(postid)]
        except KeyError:
            pass
        
def removepost(fliter,db):
    for post in db.posts.find(fliter):
        db.users.update({'postmark':post['_id']},
                {'$pull':{'postmark':post['_id']}},multi=True)
        db.users.update({'notification.postid':post['_id']},{'$pull':{'notification':{'postid':post['_id']}}},multi=True)
        for tag in post['tags']:
            db.tags.update({'name':tag},{'$inc':{'count':-1}})
    db.posts.remove(fliter)