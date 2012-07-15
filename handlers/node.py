#coding=utf-8

import tornado.web
from . import BaseHandler


class NodeHandler(BaseHandler):
    def get(self, node_name):
        node = self.get_node(node_name)
        self.render('node.html', node=node)


class CreateTopicHandler(BaseHandler):
    def get(self, node_name):
        node = self.get_node(node_name)

    def post(self):
        node = self.get_node(node_name)


class AddHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.check_role()
        self.render('node_add.html')

    @tornado.web.authenticated
    def post(self):
        self.check_role()
        name = self.get_argument('name', None)
        if not name:
            self.flash('Please fill the required field')
        if self.db.nodes.find_one({'name_lower': name.lower()}):
            self.flash('This node name is already registered')
        if self.messages:
            self.render('node_add.html')
            return

        description = self.get_argument('description', '')
        html = self.get_argument('html', '')
        self.db.nodes.insert({
            'name': name,
            'name_lower': name.lower(),
            'description': description,
            'html': html,
        })
        self.redirect('/node/' + name)


class EditHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, node_name):
        self.check_role()
        node = self.get_node(node_name)
        self.render('node_edit.html', node=node)

    @tornado.web.authenticated
    def post(self, node_name):
        self.check_role()
        node = self.get_node(node_name)
        node['description'] = self.get_argument('description', '')
        node['html'] = self.get_argument('html', '')
        self.db.nodes.save(node)

        self.flash('Save successfully', type='success')
        self.redirect('/node/' + node_name)


class RemoveHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, node_name):
        self.check_role()
        pass

    @tornado.web.authenticated
    def post(self, node_name):
        self.check_role()
        pass


handlers = [
    (r'/node/add', AddHandler),
    (r'/node/(\w+)', NodeHandler),
    (r'/node/(\w+)', CreateTopicHandler),
    (r'/node/(\w+)/edit', EditHandler),
    (r'/node/(\w+)/remove', RemoveHandler),
]
