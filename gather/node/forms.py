# -*- coding:utf-8 -*-

from __future__ import unicode_literals

from gather.form import Form
from wtforms import TextField, TextAreaField
from wtforms.validators import DataRequired, Optional, Length, URL
from .models import db, Node


class ChangeNodeForm(Form):
    name = TextField("节点名称", validators=[
        DataRequired()
    ])
    slug = TextField("Slug", validators=[
        DataRequired()
    ], description="就是会出现在 URL 里面的那坨字母~"
    )
    description = TextAreaField("简介", validators=[
        Optional(), Length(max=500)
    ], description="喵")
    icon = TextField("节点图标", validators=[
        Optional(), URL()
    ])

    def save(self, node):
        self.populate_obj(node)
        db.session.add(node)
        db.session.commit()


class CreateNodeForm(ChangeNodeForm):
    def validate_name(self, field):
        if Node.query.filter_by(name=field.data.lower()).count():
            raise ValueError("这个节点名被注册了")

    def validate_slug(self, field):
        if Node.query.filter_by(slug=field.data.lower()).count():
            raise ValueError("这个 Slug 被注册了")

    def create(self):
        node = Node(**self.data)
        self.node = node
        db.session.add(node)
        db.session.commit()
