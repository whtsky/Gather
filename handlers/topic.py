#coding=utf-8

from . import BaseHandler


class TopicHandler(BaseHandler):
    def get(self, topic_id):
        topic = self.get_topic(topic_id)
        self.render('topic.html', topic=topic)


class ReplyHandler(BaseHandler):
    def topic(self, topic_id):
        pass


class RemoveHandler(BaseHandler):
    def get(self, topic_id):
        pass


class MoveHandler(BaseHandler):
    def get(self, topic_id):
        topic = self.get_topic(topic_id)
        self.render('topic_move.html', topic=topic)

    def topic(self, topic_id):
        pass


class StarHandler(BaseHandler):
    def get(self, topic_id):
        pass


class UnstarHandler(BaseHandler):
    def get(self, topic_id):
        pass


handlers = [
    (r'/topic/(\w+)', TopicHandler),
    (r'/topic/(\w+)/reply', ReplyHandler),
    (r'/topic/(\w+)/remove', RemoveHandler),
    (r'/topic/(\w+)/move', MoveHandler),
    (r'/topic/(\w+)/star', StarHandler),
    (r'/topic/(\w+)/unstar', UnstarHandler),
]
