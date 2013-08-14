# coding=utf-8

from bson.objectid import ObjectId
from . import BaseHandler as _BaseHandler


class BaseHandler(_BaseHandler):
    def prepare(self):
        self.check_role(role_min=3)
        super(BaseHandler, self).prepare()


class LinkHandler(BaseHandler):
    def get(self):
        self.render('dashboard/link.html')

    def post(self):
        name = self.get_argument('name', None)
        link = self.get_argument('link', None)
        title = self.get_argument('title', '')
        priority = int(self.get_argument('priority', 1))
        if not (name and link and priority):
            self.flash('Please fill the required field')
        if link and self.db.links.find_one({'link': link.lower()}):
            self.flash('This link has been registered')
        if self.messages:
            self.redirect('/dashboard/link')
        self.db.links.insert({
            'name': name,
            'link': link,
            'title': title,
            'priority': priority,
        })
        self.redirect('/dashboard/link')


class RemoveLinkHandler(BaseHandler):
    def get(self, link_id):
        self.db.links.remove(ObjectId(link_id))
        self.redirect('/dashboard/link')


handlers = [
    (r'/dashboard/link', LinkHandler),
    (r'/dashboard/link/(\w+)/remove', RemoveLinkHandler),
]
