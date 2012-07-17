#coding=utf-8

import tornado.web
from . import BaseHandler


class MemberListHandler(BaseHandler):
    def get(self):
        pass


class MemberPageHandler(BaseHandler):
    def get(self, name):
        member = self.get_member(name)
        topics = self.db.topics.find({'author': member['name']},
            sort=[('last_reply_time', -1)])
        topics = topics[:self.settings['topics_per_page']]
        replies = self.db.replies.find({'author': member['name']},
            sort=[('index', 1)])
        replies = replies[:self.settings['replies_per_page']]
        if member['like']:
            member['like'] = member['like'][:self.settings['topics_per_page']]
            liked_topics = [self.get_topic(x) for x in member['like']]
        else:
            liked_topics = []
        self.render('member/member.html', member=member, topics=topics,
            replies=replies, liked_topics=liked_topics)


class MemberTopicsHandler(BaseHandler):
    def get(self, name):
        member = self.get_member(name)
        topics = self.db.topics.find({'author': member['name']},
            sort=[('last_reply_time', -1)])
        topics_count = topics.count()
        p = int(self.get_argument('p', 1))
        topics = topics[(p - 1) * self.settings['topics_per_page']:
            p * self.settings['topics_per_page']]
        self.render('member/topics.html', member=member,
            topics=topics, topics_count=topics_count, p=p)


class BlockHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, name):
        self.db.members.update({'_id': self.current_user['_id']},
                {'$addToSet': {'block': name.lower()}})
        self.redirect('/')


class UnblockHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, name):
        self.current_user['block'].remove(name.lower())
        self.db.members.save(self.current_user)
        self.redirect('/member/' + name)


class RemoveHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, name):
        member = self.get_member(name)
        self.check_role(owner_name=member['name'])
        member_id = member['_id']
        self.application.db.posts.remove({'author': member_id})
        self.application.db.replies.remove({'author': member_id})
        self.application.db.members.remove({'_id': member_id})


class SetRoleHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self, name):
        pass

handlers = [
    (r'/member/(\w+)', MemberPageHandler),
    (r'/member/(\w+)/topics', MemberTopicsHandler),
    (r'/member/(\w+)/block', BlockHandler),
    (r'/member/(\w+)/unblock', UnblockHandler),
    (r'/member/(\w+)/remove', RemoveHandler),
    (r'/member/(\w+)/role', SetRoleHandler),
]
