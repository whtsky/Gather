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
from .models import Topic, Reply, History


class CreateTopicForm(Form):
    node = QuerySelectField(
        "节点",
        validators=[Required()],
        query_factory=Node.query_all,
        get_pk=lambda a: a.id,
        get_label=lambda a: a.name
    )
    title = TextField("标题", validators=[
        Required(),
        Length(max=100)
    ])
    content = TextAreaField("正文", validators=[Optional()])

    def create(self):
        topic = Topic(
            author=g.user,
            **self.data
        )
        return topic.save()


class ChangeTopicForm(CreateTopicForm):
    def save(self, topic):
        if self.title.data != topic.title:
            title = self.title.data
            history = History(
                diff_content="将标题从 %s 修改为 %s" % (topic.title, title),
                topic=topic,
                author=g.user
            )
            history.save()
            topic.title = title
        if self.node.data != topic.node:
            node = self.node.data
            history = History(
                diff_content="从 %s 移动到 %s" % (topic.node.name, node.name),
                topic=topic,
                author=g.user
            )
            history.save()
            topic.node = node
        if self.content.data != topic.content:
            content = self.content.data
            history = History(
                diff_content=diff(topic.content, content, css=False),
                topic=topic,
                author=g.user
            )
            history.save()
            topic.content = content
        topic.changed = datetime.utcnow()
        return topic.save()


class ReplyForm(Form):
    content = TextAreaField("正文", [
        Required(),
        Length(max=10000),
    ])

    def create(self, topic):
        reply = Reply(
            content=self.content.data,
            topic=topic,
            author=g.user
        )
        return reply.save()


class ChangeReplyForm(ReplyForm):
    def save(self, reply):
        if self.content.data != reply.content:
            content = self.content.data
            history = History(
                diff_content=diff(reply.content, content, css=False),
                reply=reply,
                author=g.user
            )
            history.save()
            reply.content = content
        return reply.save()
