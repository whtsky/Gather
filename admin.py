#coding=utf-8

from common import BaseHandler
from config import admin

class RemoveUserHandler(BaseHandler):
    def get(self,username):
        assert self.get_current_user() in admin
        self.db.users.remove({'username':username})
        for post in self.db.posts.find({'author':username}):
            for tag in post['tags']:
               self.db.tags.update({'name':tag},{'$inc':{'count':-1}})
        self.db.posts.remove({'author':username})
        self.db.posts.update({'comments.author':username},{'$pull':{'author':username}}):
        self.write('done.')

class RemovePostHandler(BaseHandler):
    def get(self,postid):
        assert self.get_current_user() in admin
        postid = int(postid)
        for post in self.db.posts.find({'_id':postid}):
            for tag in post['tags']:
                self.db.tags.update({'name':tag},{'$inc':{'count':-1}})
        self.db.posts.remove({'_id':postid})
        self.write('done.')

class RemoveCommentHandler(BaseHandler):
    def get(self,postid,commentid):
        assert self.get_current_user() in admin
        postid = int(postid)
        comments = self.db.posts.find_one({'_id':postid})['comments']
        del comments[int(commentid)-1]
        self.db.posts.update({'_id':postid},
                            {'$set':{'comments':comments}})
        self.write('done.')