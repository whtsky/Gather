#coding=utf-8

from . import BaseHandler


class PostHandler(BaseHandler):
    def get(self, post_id):
        post = self.get_post(post_id)
        self.render('post.html', post=post)


class ReplyHandler(BaseHandler):
    def post(self, post_id):
        pass


class RemoveHandler(BaseHandler):
    def get(self, post_id):
        pass


class MoveHandler(BaseHandler):
    def get(self, post_id):
        post = self.get_post(post_id)
        self.render('post_move.html', post=post)

    def post(self, post_id):
        pass


class StarHandler(BaseHandler):
    def get(self, post_id):
        pass


class UnstarHandler(BaseHandler):
    def get(self, post_id):
        pass


handlers = [
    (r'/post/(\w+)', PostHandler),
    (r'/post/(\w+)/reply', ReplyHandler),
    (r'/post/(\w+)/remove', RemoveHandler),
    (r'/post/(\w+)/move', MoveHandler),
    (r'/post/(\w+)/star', StarHandler),
    (r'/post/(\w+)/unstar', UnstarHandler),
]
