#coding=utf-8

from . import BaseHandler


class NodeHandler(BaseHandler):
    def get(self, node_name):
        node = self.application.db.nodes.find_one({'name': node_name})
        self.render('node.html', node=node)


class AddHandler(BaseHandler):
    def get(self):
        self.render('node_add.html')

    def post(self):
        pass


handlers = [
    (r'/node/(\w+)', NodeHandler),
    (r'/node/add', AddHandler),
]
