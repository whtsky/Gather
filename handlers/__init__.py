#coding=utf-8

import tornado.web
import hashlib


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        password = self.get_secure_cookie('user')
        return self.application.db.users.find_one({'password': password})

    @property
    def db(self):
        return self.application.db

    def get_member(self, name):
        name = name.lower()
        member = self.db.members.find_one({'name_lower': name})
        if not member:
            raise tornado.web.HTTPError(404)
        #TODO: ADD GAVATAR URI.
        return member

    def get_post(self, post_id):
        post = self.db.posts.find_one({'_id': post_id})
        if not post:
            raise tornado.web.HTTPError(404)
        return post
