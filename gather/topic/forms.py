# -*- coding:utf-8 -*-

from __future__ import unicode_literals

from datetime import datetime
from flask import g
from gather.form import Form
from wtforms import TextField, TextAreaField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import Required, Optional, Length
from ghdiff import diff
from gather.node.models import Node
from .models import db, Topic, Reply, History


class CreateTopicForm(Form):
    node_id = QuerySelectField(
        "节点",
        validators=[Required()],
        query_factory=Node.cached_node_list,
        get_pk=lambda a: a[0],
        get_label=lambda a: a[1]
    )
    title = TextField("标题", validators=[
        Required(),
        Length(max=30)
    ])
    content = TextAreaField("正文", validators=[Optional()])

    def create(self):
        topic = Topic(
            title=self.title.data,
            content=self.content.data,
            node_id=self.node_id.data[0],
            author=g.user,
        )
        db.session.add(topic)
        db.session.commit()
        return topic


class ChangeTopicForm(CreateTopicForm):
    def save(self, topic):
        if self.title.data != topic.title:
            title = self.title.data
            history = History(
                diff_content="将标题从 %s 修改为 %s" % (topic.title, title),
                topic=topic,
                author=g.user
            )
            db.session.add(history)
            topic.title = title
        if self.node_id.data != topic.node_id:
            node = Node.query.get_or_404(self.node_id.data[0])
            history = History(
                diff_content="从 %s 移动到 %s" % (topic.node.name, node.name),
                topic=topic,
                author=g.user
            )
            db.session.add(history)
            topic.node = node
        if self.content.data != topic.content:
            content = self.content.data
            history = History(
                diff_content=diff(topic.content, content, css=False),
                topic=topic,
                author=g.user
            )
            db.session.add(history)
            topic.content = content
        topic.changed = datetime.now()
        db.session.add(topic)
        db.session.commit()
        return topic


class ReplyForm(Form):
    content = TextAreaField("正文", validators=[Required()])

    def create(self, topic):
        reply = Reply(
            content=self.content.data,
            topic_id=topic.id,
            author=g.user
        )
        topic.updated = datetime.now()
        db.session.add(reply)
        db.session.commit()
        return reply


class ChangeReplyForm(Form):
    content = TextAreaField(
        "正文", [
            Required(),
            Length(min=3, max=1000000),
        ],
    )

    def save(self, reply):
        if self.content.data != reply.content:
            content = self.content.data
            history = History(
                diff_content=diff(reply.content, content, css=False),
                reply=reply,
                author=g.user
            )
            db.session.add(history)
            reply.content = content
        db.session.add(reply)
        db.session.commit()
        return reply