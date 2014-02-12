# -*- coding:utf-8 -*-

from __future__ import unicode_literals

import datetime

from pymongo import MongoClient
from gather import create_app
from gather.extensions import db
from gather.account.models import Account
from gather.node.models import Node
from gather.topic.models import Topic, Reply

app = create_app()

mongo_database = MongoClient()["forum"]


def role(num):
    if num == 1:
        return "user"
    elif num >= 5:
        return "admin"
    return "staff"


def timestamp_to_datetime(t):
    return datetime.datetime.fromtimestamp(t)


def main():
    for pbb_member in mongo_database.members.find(sort=[('created', 1)]):
        account = Account(
            username=pbb_member["name"].lower(),
            email=pbb_member["email"],
            website=pbb_member["website"],
            description=pbb_member["description"],
            role=role(pbb_member["role"]),
            created=timestamp_to_datetime(pbb_member["created"]),
            password="need-to-reset"
        )
        print "Migrating Account %s" % account.username
        account.create_password(str(pbb_member["_id"]))
        db.session.add(account)
        db.session.commit()

    for pbb_node in mongo_database.nodes.find():
        node = Node(
            name=pbb_node["title"],
            slug=pbb_node["name"].lower(),
            description=pbb_node["description"]
        )
        db.session.add(node)
        db.session.commit()

    for pbb_topic in mongo_database.topics.find(sort=[('last_reply_time', 1)]):
        topic = Topic(
            title=pbb_topic["title"],
            content=pbb_topic["content"],
            author=Account.query.filter_by(username=pbb_topic["author"].lower()).first(),
            node=Node.query.filter_by(name=pbb_topic["node"].lower()).first(),
            created=timestamp_to_datetime(pbb_topic["created"]),
            updated=timestamp_to_datetime(pbb_topic["last_reply_time"])
        )
        print "Migrating Topic %s by %s" % (topic.title, topic.author.username)
        db.session.add(topic)
        db.session.commit()
        for pbb_reply in mongo_database.replies.find({'topic': str(pbb_topic["_id"])},
                                                     sort=[('index', 1)]):
            reply = Reply(
                content=pbb_reply["content"],
                author=Account.query.filter_by(username=pbb_reply["author"].lower()).first(),
                topic=topic,
                created=timestamp_to_datetime(pbb_reply["created"])
            )
            print "Migrating Reply %s by %s" % (reply.content, reply.author.username)

            db.session.add(reply)
        db.session.commit()


with app.app_context():
    db.drop_all()
    db.create_all()
    main()
