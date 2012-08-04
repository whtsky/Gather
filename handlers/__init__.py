#coding=utf-8

import re
import tornado.web
import tornado.escape
import tornado.locale
import time
from bson.objectid import ObjectId
import hashlib
from .recaptcha import RecaptchaMixin

_MENTION_FINDER_ = re.compile('class="mention">@(\w+)')


class BaseHandler(tornado.web.RequestHandler, RecaptchaMixin):
    def prepare(self):
        if self.request.remote_ip != '127.0.0.1' and \
           self.request.host != self.settings['host']:
            self.redirect(self.settings['forum_url'] + self.request.uri[1:],
                permanent=True)

        messages = self.get_secure_cookie('flash_messages')
        self.messages = messages and tornado.escape.json_decode(messages) or []

    def get_current_user(self):
        password = self.get_secure_cookie('user')
        member = self.application.db.members.find_one({'password': password})
        if member and member['role'] < 0:
            self.flash('Your account has been deactived.')
            self.clear_cookie('user')
            return None
        return member

    def get_user_locale(self):
        if not self.current_user:
            return None
        return tornado.locale.get(self.current_user['language'])

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
        return '<a href="/member/%s" class="avatar">\
            <img src="%s" /></a>' % (member['name'], avatar)

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
        now = time.gmtime(time.time() + offset)
        date = time.strftime('%Y-%m-%d', t)
        if date == time.strftime('%Y-%m-%d', now):
            return time.strftime('%H:%M:%S', t)
        return date

    def send_notification(self, content, topic_id):
        uname = self.current_user['name_lower']
        for name in set(_MENTION_FINDER_.findall(content)):
            member = self.db.members.find_one({'name_lower': name.lower()})
            if not member:
                continue
            if uname in member['block'] or uname == member['name_lower']:
                continue
            self.db.notifications.insert({
                'topic': topic_id,
                'from': uname,
                'to': member['name_lower'],
                'content': content,
                'read': False,
                'created': time.time(),
            })
