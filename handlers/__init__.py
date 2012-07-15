#coding=utf-8

import tornado.web
import hashlib


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        password = self.get_secure_cookie('user')
        return self.application.db.members.find_one({'password': password})

    def get_user_locale(self):
        return self.current_user and self.current_user['locale'] or None

    @property
    def db(self):
        return self.application.db

    def get_member(self, name):
        name = name.lower()
        member = self.db.members.find_one({'name_lower': name})
        if not member:
            raise tornado.web.HTTPError(404)
        hashed_email = hashlib.md5(member['email']).hexdigest()
        member['gravatar'] = self.settings['gravatar_base_url'] + hashed_email
        return member

    def get_topic(self, topic_id):
        topic = self.db.topics.find_one({'_id': topic_id})
        if not topic:
            raise tornado.web.HTTPError(404)
        return topic
