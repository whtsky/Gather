# -*- coding:utf-8 -*-

from __future__ import unicode_literals
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from gather.form import Form
from wtforms import TextField, TextAreaField
from wtforms.validators import DataRequired, Optional, Length, URL
from .models import Node


class ChangeNodeForm(Form):
    name = TextField("节点名称", validators=[
        DataRequired()
    ])
    slug = TextField("Slug", validators=[
        DataRequired()
    ], description="就是会出现在 URL 里面的那坨字母~"
    )
    parent_node = QuerySelectField(
        "父节点",
        validators=[Optional()],
        query_factory=Node.query_all,
        get_pk=lambda a: a.id,
        get_label=lambda a: a.name,
        allow_blank=True
    )
    description = TextAreaField("简介", validators=[
        Optional(), Length(max=500)
    ], description="喵")
    icon = TextField("节点图标", validators=[
        Optional(), URL()
    ])

    def validate_parent_node(self, field):
        if field.data == self.obj:
            raise ValueError("父节点不能是自己= =")

    def save(self):
        node = self.obj
        self.populate_obj(node)
        return node.save()


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
        return node.save()
