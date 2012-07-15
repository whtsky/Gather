#coding=utf-8

import tornado.web
from . import BaseHandler


class NodeHandler(BaseHandler):
    def get(self, node_name):
        node = self.get_node(node_name)
        self.render('node/node.html', node=node)


class CreateTopicHandler(BaseHandler):
    def get(self, node_name):
        node = self.get_node(node_name)

    def post(self):
        node = self.get_node(node_name)


class AddHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.check_role()
        self.render('node/add.html')

    @tornado.web.authenticated
    def post(self):
        self.check_role()
        name = self.get_argument('name', None)
        if not name:
            self.flash('Please fill the required field')
        if self.db.nodes.find_one({'name_lower': name.lower()}):
            self.flash('This node name is already registered')
        if self.messages:
            self.render('node/add.html')
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
        self.render('node/edit.html', node=node)

    @tornado.web.authenticated
    def post(self, node_name):
        self.check_role()
        node = self.get_node(node_name)
        node['description'] = self.get_argument('description', '')
        node['html'] = self.get_argument('html', '')
        self.db.nodes.save(node)

        self.flash('Save successfully', type='success')
        self.redirect('/node/' + node['name'])


class RemoveHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, node_name):
        self.check_role()
        pass

    @tornado.web.authenticated
    def post(self, node_name):
        self.check_role()
        pass


class FavoriteHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, node_name):
        node = self.get_node(node_name)
        user_id = self.current_user['_id']
        self.db.members.update({'_id': user_id},
                {'$addToSet': {'favorite': node['name']}})
        self.redirect('/node/' + node['name'])


class UnfavoriteHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, node_name):
        node = self.get_node(node_name)
        user = self.current_user
        user['favorite'].remove(node['name'])
        self.db.members.save(user)
        self.redirect('/node/' + node['name'])


class NodeSidebar(tornado.web.UIModule):
    def render(self, node):
        return self.render_string("node/modules/sidebar.html", node=node)

handlers = [
    (r'/node/add', AddHandler),
    (r'/node/(\w+)', NodeHandler),
    (r'/node/(\w+)/create', CreateTopicHandler),
    (r'/node/(\w+)/edit', EditHandler),
    (r'/node/(\w+)/remove', RemoveHandler),
    (r'/node/(\w+)/favorite', FavoriteHandler),
    (r'/node/(\w+)/unfavorite', UnfavoriteHandler),
]

ui_modules = {
    'node_sitebar': NodeSidebar,
}