#coding=utf-8

from . import BaseHandler


class TopicHandler(BaseHandler):
    def get(self, topic_id):
        topic = self.get_topic(topic_id)
        self.render('topic/topic.html', topic=topic)


class ReplyHandler(BaseHandler):
    def topic(self, topic_id):
        pass


class RemoveHandler(BaseHandler):
    def get(self, topic_id):
        pass


class MoveHandler(BaseHandler):
    def get(self, topic_id):
        topic = self.get_topic(topic_id)
        self.render('topic/move.html', topic=topic)

    def topic(self, topic_id):
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
