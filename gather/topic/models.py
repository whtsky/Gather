# -*- coding:utf-8 -*-

from datetime import datetime
from gather.account.models import Account
from gather.node.models import Node
from gather.extensions import db


class Topic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text(), nullable=True, default="")
    author_id = db.Column(
        db.Integer,
        db.ForeignKey('account.id'), index=True, nullable=False
    )
    author = db.relationship(Account)
    node_id = db.Column(
        db.Integer,
        db.ForeignKey('node.id'), index=True, nullable=False
    )
    node = db.relationship(Node)
    created = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    replies = db.relationship("Reply", lazy='dynamic')
    updated = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )
    changed = db.Column(
        db.DateTime,
        nullable=True
    )

    def __str__(self):
        return self.title

    def __repr__(self):
        return '<Topic: %s>' % self.title


class Reply(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text(), nullable=True, default="")
    author_id = db.Column(
        db.Integer,
        db.ForeignKey('account.id'), nullable=False
    )
    author = db.relationship(Account)
    topic_id = db.Column(
        db.Integer,
        db.ForeignKey('topic.id'), index=True, nullable=False
    )
    topic = db.relationship(Topic)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    changed = db.Column(
        db.DateTime,
        nullable=True,
        onupdate=datetime.utcnow
    )


class History(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    diff_content = db.Column(db.Text(), nullable=True, default="")
    author_id = db.Column(db.Integer, db.ForeignKey('account.id'))
    author = db.relationship(Account)
    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'), index=True)
    topic = db.relationship(Topic)
    reply_id = db.Column(db.Integer, db.ForeignKey('reply.id'), index=True)
    reply = db.relationship(Reply)
    created = db.Column(db.DateTime, default=datetime.utcnow)
