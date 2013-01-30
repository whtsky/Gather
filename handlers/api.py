import re
import tornado.web
import tornado.escape

from . import BaseHandler

html_re = re.compile('(<.*?>)')


class NewNotificationsHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        notifications = []
        notis = self.db.notifications.find({
            'to': self.current_user['name_lower'],
            'read': False
        }, sort=[('created', -1)])
        for noti in notis:
            member = self.get_member(noti['from'])
            topic = self.get_topic(noti['topic'])
            content = html_re.sub('', noti['content'])
            content = tornado.escape.xhtml_unescape(content)
            notifications.append({
                'avatar': self.get_avatar(member),
                'title': '%s mentioned you' % member['name'],
                'content': content,
                'url': '/topic/%s' % topic['_id']
            })

        # Turn to json.
        self.write({
            "notifications": notifications
        })
        # https://github.com/facebook/tornado/blob/master/tornado/web.py#L501


handlers = [
    (r'/api/notifications/new', NewNotificationsHandler),
]
