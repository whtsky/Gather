# coding=utf-8

import re
import tornado.web
import tornado.escape
import tornado.locale
import time
import hashlib
import ghdiff

from raven.contrib.tornado import SentryMixin
from bson.objectid import ObjectId

from .recaptcha import RecaptchaMixin

_MENTION_FINDER_ = re.compile('class="mention">@(\w+)')
_NOKIA_FINDER_ = re.compile('(Nokia.*?)/')


class BaseHandler(tornado.web.RequestHandler, RecaptchaMixin, SentryMixin):
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

    def get_source(self):
        ua = self.request.headers.get("User-Agent", "bot")
        sources = dict(
            iPod='iPod',
            iPhone='iPhone',
            iPad='iPad',
            Android='Android',
            Kindle='Kindle',
            BlackBerry='BlackBerry',
            TouchPad='TouchPad',
            silk='Kindle Fire',
        )
        for k, v in sources.items():
            if k in ua:
                return v
        if 'Windows Phone' in ua:
            return 'Windows Phone'
        if 'Nokia' in ua:
            return _NOKIA_FINDER_.findall(ua)[0]

        return None

    @property
    def db(self):
        return self.application.db

    @property
    def messages(self):
        if not hasattr(self, '_messages'):
            messages = self.get_secure_cookie('flash_messages')
            self._messages = []
            if messages:
                self._messages = tornado.escape.json_decode(messages)
        return self._messages

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
        size *= 2  # Retina
        url = self.get_avatar_img(member, size)
        return '<a href="/member/%s" class="avatar">\
            <img src="%s" /></a>' % (member['name'], url)

    def get_avatar_img(self, member, size=48):
        hashed_email = hashlib.md5(member['email']).hexdigest()
        url = self.settings['gravatar_base_url'] + hashed_email
        url += '?s=%s' % size
        return url

    def get_page_num(self, count, per_page):
        return int((count + per_page - 1) / per_page)

    def flash(self, message, type='error'):
        self.messages.append((type, message))
        self.set_secure_cookie('flash_messages',
                               tornado.escape.json_encode(self.messages))

    def get_flashed_messages(self):
        messages = self.messages
        self._messages = []
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
        t = time.gmtime(t)
        utc = time.strftime('%Y-%m-%dT%H:%M:%SZ', t)
        htm = '<time datetime="%s"></time>' % utc
        return htm

    def send_notification(self, content, topic_id):
        if not isinstance(topic_id, ObjectId):
            topic_id = ObjectId(topic_id)
        uname = self.current_user['name_lower']
        for name in set(_MENTION_FINDER_.findall(content)):
            member = self.db.members.find_one({'name_lower': name.lower()})
            if not member:
                continue
            if uname == member['name_lower']:
                continue
            self.db.notifications.insert({
                'topic': topic_id,
                'from': uname,
                'to': member['name_lower'],
                'content': content,
                'read': False,
                'created': time.time(),
            })

    def save_history(self, id, before, after):
        data = {
            "author": self.current_user['name'],
            "before": before,
            "after": after,
            "ghdiff": ghdiff.diff(before, after, css=False),
            "target_id": ObjectId(id),
            "created": time.time()
        }
        self.db.histories.insert(data)
