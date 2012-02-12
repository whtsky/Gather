#coding=utf-8

from common import BaseHandler
from config import admin

class RemoveUserHandler(BaseHandler):
    def get(self,username):
        assert self.get_current_user() in admin
        self.db.users.remove({'username':username})
        for post in self.db.posts.find({'author':post}):
            for tag in post['tags']:
               self.db.tags.update({'name':tag},{'$inc':{'count':-1}})
        self.db.posts.remove({'author':post})
        for post in self.db.posts.find({'comments.author':username}):
            comments = []
            for comment in post['comments']:
                if comment['author']!=username:
                    comments.append(comment)
            self.db.posts.update({'_id':post['_id']},{'$set':{'comments':comment}})
        self.write('done.')