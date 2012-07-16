#coding=utf-8

import tornado.web
from . import BaseHandler
from .utils import make_content, utc_time


class NodeHandler(BaseHandler):
    def get(self, node_name):
        node = self.get_node(node_name)
        topics = self.db.topics.find({'node': node['name']})
        topics_count = topics.count()
        p = int(self.get_argument('p', 1))
        self.render('node/node.html', node=node, topics=topics,
            topics_count=topics_count, p=p)


class CreateTopicHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, node_name):
        node = self.get_node(node_name)
        self.render('node/create.html', node=node)

    @tornado.web.authenticated
    def post(self, node_name):
        node = self.get_node(node_name)
        title = self.get_argument('title', '')
        content = self.get_argument('content', '')
        if not (title and content):
            self.flash('Please fill the required field')
        if len(title) > 100:
            self.flash("The title is too long")
        if self.messages:
            self.render('node/create.html', node=node)
            return
        topic = self.db.topics.find_one({
            'title': title,
            'content': content,
            'author': self.current_user['_id']
        })
        if topic:
            self.redirect('/topic/%s' % topic['_id'])
            return
        time_now = utc_time()
        topic_id = self.db.topics.insert({
            'title': title,
            'content': content,
            'content_html': make_content(content),
            'author': self.current_user['name'],
            'node': node['name'],
            'created': time_now,
            'modified': time_now,
            'reply_count': 0,
        })
        self.redirect('/topic/%s' % topic_id)


class AddHandler(BaseHandler):
    def get(self):
        self.check_role()
        self.render('node/add.html')

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
    def get(self, node_name):
        self.check_role()
        node = self.get_node(node_name)
        self.render('node/edit.html', node=node)

    def post(self, node_name):
        self.check_role()
        node = self.get_node(node_name)
        node['description'] = self.get_argument('description', '')
        node['html'] = self.get_argument('html', '')
        self.db.nodes.save(node)

        self.flash('Saved successfully', type='success')
        self.redirect('/node/' + node['name'])


class RemoveHandler(BaseHandler):
    def get(self, node_name):
        self.check_role()
        pass

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
    (r'/node/([%A-Za-z0-9.]+)', NodeHandler),
    (r'/node/([%A-Za-z0-9.]+)/create', CreateTopicHandler),
    (r'/node/([%A-Za-z0-9.]+)/edit', EditHandler),
    (r'/node/([%A-Za-z0-9.]+)/remove', RemoveHandler),
    (r'/node/([%A-Za-z0-9.]+)/favorite', FavoriteHandler),
    (r'/node/([%A-Za-z0-9.]+)/unfavorite', UnfavoriteHandler),
]

ui_modules = {
    'node_sitebar': NodeSidebar,
}
