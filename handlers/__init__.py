#coding=utf-8

import re
import tornado.web
import tornado.escape
import time
from pymongo.objectid import ObjectId
import hashlib

_MENTION_FINDER_ = re.compile('class="mention">@(\w+)')


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
        topic = self.db.topics.find_one({'_id': ObjectId(topic_id)})
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

    def check_role(self, role_min=2, owner_name='', return_bool=False):
        user = self.current_user
        if user and (user['name'] == owner_name or user['role'] >= role_min):
            return True
        if return_bool:
            return False
        raise tornado.web.HTTPError(403)

    def format_time(self, t):
        offset = self.settings['gmt_offset'] * 3600
        t = time.gmtime(t + offset)
        date = time.strftime('%Y-%m-%d', t)
        if date == time.strftime('%Y-%m-%d', time.gmtime(time.time() + offset)):
            return time.strftime('%H:%M:%S', t)
        return date

    def send_notification(self, content, topic_id):
        name = self.current_user['name_lower']
        for name in _MENTION_FINDER_.findall(content):
            member = self.get_member(name)
            if name in member['block'] or name == member['name_lower']:
                continue
            self.db.notifications.insert({
                'topic': topic_id,
                'from': name,
                'to': member['name_lower'],
                'content': content,
                'read': False,
                'created': time.time(),
            })

