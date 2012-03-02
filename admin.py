#coding=utf-8

from common import BaseHandler
from config import admin

class RemoveUserHandler(BaseHandler):
    def get(self,username):
        assert self.get_current_user()['username'] in admin
        removepost(fliter={'author':username},db=self.db)
        self.db.users.remove({'username':username})
        self.db.posts.update({'comments.author':username},
                {'$pull':{'comments':{'author':username}}},multi=True)
        self.write('done.')

class RemovePostHandler(BaseHandler):
    def get(self,postid):
        assert self.get_current_user()['username'] in admin
        postid = int(postid)
        removepost(fliter={'_id':postid},db=self.db)
        self.write('done.')

class RemoveCommentHandler(BaseHandler):
    def get(self,postid,commentid):
        assert self.get_current_user()['username'] in admin
        self.db.posts.update({'_id':int(postid)},
                            {'$pop':{'comments':int(commentid)-1}})
        self.write('done.')
        
def removepost(fliter,db):
    for post in db.posts.find(fliter):
        db.users.update({'postmark':post['_id']},
                {'$pull':{'postmark':post['_id']}},multi=True)
        for tag in post['tags']:
            db.tags.update({'name':tag},{'$inc':{'count':-1}})
    db.posts.remove(fliter)