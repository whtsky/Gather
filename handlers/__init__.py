#coding=utf-8

import tornado.web
import tornado.escape
import hashlib


class BaseHandler(tornado.web.RequestHandler):
    def prepare(self):
        messages = self.get_secure_cookie('flash_messages')
        self.messages = messages and tornado.escape.json_decode(messages) or []

    def get_current_user(self):
        password = self.get_secure_cookie('user')
        return self.application.db.members.find_one({'password': password})

    @property
    def db(self):
        return self.application.db

    def get_member(self, name):
        name = name.lower()
        member = self.db.members.find_one({'name_lower': name})
        if not member:
            raise tornado.web.HTTPError(404)
        return member

    def get_topic(self, topic_id):
        topic = self.db.topics.find_one({'_id': topic_id})
        if not topic:
            raise tornado.web.HTTPError(404)
        return topic

    def get_node(self, node_name):
        node_name = node_name.lower()
        node = self.db.nodes.find_one({'name_lower': node_name})
        if not node:
            raise tornado.web.HTTPError(404)
        return node

    def get_avatar(self, member, size=48):
        hashed_email = hashlib.md5(member['email']).hexdigest()
        avatar = self.settings['gravatar_base_url'] + hashed_email
        avatar += '?s=%s' % size
        return avatar


    def flash(self, message, type='error'):
        self.messages.append((type, message))
        self.set_secure_cookie('flash_messages',
            tornado.escape.json_encode(self.messages))

    def get_flashed_messages(self):
        messages = self.messages
        self.messages = []
        self.clear_cookie('flash_messages')
        return messages

    def check_role(self, role_min=2):
        if self.current_user['role'] < role_min:
            raise tornado.web.HTTPError(403)
