#coding=utf-8

import tornado.web
from . import BaseHandler
from .utils import make_content, utc_time


class TopicHandler(BaseHandler):
    def get(self, topic_id):
        topic = self.get_topic(topic_id)
        self.render('topic/topic.html', topic=topic)


class ReplyHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self, topic_id):
        content = self.get_argument('content', None)
        if not content:
            self.flash('Please fill the required field')
            self.redirect('/topic/%s' % topic_id)
            return
        reply = self.db.replies.find_one({
            'topic': topic_id,
            'content': content,
            'author': self.current_user['_id']
        })
        if reply:
            self.redirect('/topic/%s' % topic_id)
            return
        index = self.db.topics.find_and_modify({'_id': topic_id},
            update={'$inc': {'reply_count': 1}})['reply_count'] + 1
        time_now = utc_time()
        self.db.replies.insert({
            'content': content,
            'content_html': make_content(content),
            'author': self.current_user['_id'],
            'topic': topic_id,
            'created': time_now,
            'modified': time_now,
            'index': index,
        })
        self.redirect('/topic/%s' % topic_id)


class RemoveHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, topic_id):
        self.check_role()
        self.db.topics.remove({'_id': topic_id})
        self.db.replies.remove({'topic': topic_id})
        self.flash('Removed successfully')
        self.redirect('/')


class MoveHandler(BaseHandler):
    def get(self, topic_id):
        topic = self.get_topic(topic_id)
        self.render('topic/move.html', topic=topic)

    def post(self, topic_id):
        pass


class StarHandler(BaseHandler):
    def get(self, topic_id):
        user_id = self.current_user['_id']
        self.db.members.update({'_id': user_id},
                {'$addToSet': {'star': topic_id}})
        self.redirect('/topic/' + topic_id)


class UnstarHandler(BaseHandler):
    def get(self, topic_id):
        user = self.current_user
        user['star'].remove(topic_id)
        self.db.members.save(user)
        self.redirect('/topic/' + topic_id)

handlers = [
    (r'/topic/(\w+)', TopicHandler),
    (r'/topic/(\w+)/reply', ReplyHandler),
    (r'/topic/(\w+)/remove', RemoveHandler),
    (r'/topic/(\w+)/move', MoveHandler),
    (r'/topic/(\w+)/star', StarHandler),
    (r'/topic/(\w+)/unstar', UnstarHandler),
]
