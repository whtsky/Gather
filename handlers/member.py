#coding=utf-8

import tornado.web
from . import BaseHandler


class MemberListHandler(BaseHandler):
    def get(self):
        per_page = self.settings['members_per_page']
        members = self.db.members.find(sort=[('created', -1)])
        count = members.count()
        p = int(self.get_argument('p', 1))
        members = members[(p - 1) * per_page:p * per_page]
        self.render('member/list.html', per_page=per_page, members=members,
            count=count, p=p)


class MemberPageHandler(BaseHandler):
    def get(self, name):
        member = self.get_member(name)
        topics = self.db.topics.find({'author': member['name']},
            sort=[('last_reply_time', -1)])
        topics = topics[:self.settings['topics_per_page']]
        replies = self.db.replies.find({'author': member['name']},
            sort=[('created', -1)])
        replies = replies[:self.settings['replies_per_page']]
        if member['like']:
            member['like'] = member['like'][:self.settings['topics_per_page']]
            liked_topics = [self.get_topic(x) for x in member['like']]
        else:
            liked_topics = []
        self.render('member/member.html', member=member, topics=topics,
            replies=replies, liked_topics=liked_topics)


class FollowHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, name):
        member = self.get_member(name)
        self.db.members.update({'_id': self.current_user['_id']},
                {'$addToSet': {'follow': member['name']}})
        self.redirect('/member/%s' % name)


class UnfollowHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, name):
        member = self.get_member(name)
        self.current_user['follow'].remove(member['name'])
        self.db.members.save(self.current_user)
        self.redirect('/member/' + name)


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


class ChangeRoleHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self, name):
        role = int(self.get_argument('role', 100))
        if self.current_user['role'] < 3:
            self.check_role(role_min=role + 1)
        name = name.lower()
        self.db.members.update({'name_lower': name},
                {'$set': {'role': role}})
        self.redirect('/member/' + name)


handlers = [
    (r'/member', MemberListHandler),
    (r'/member/(\w+)', MemberPageHandler),
    (r'/member/(\w+)/topics', MemberTopicsHandler),
    (r'/member/(\w+)/follow', FollowHandler),
    (r'/member/(\w+)/unfollow', UnfollowHandler),
    (r'/member/(\w+)/role', ChangeRoleHandler),
]
