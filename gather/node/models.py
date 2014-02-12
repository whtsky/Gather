# -*- coding:utf-8 -*-

from flask.ext.sqlalchemy import models_committed
from gather.extensions import db, cache


class Node(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True, index=True)
    slug = db.Column(db.String(100), nullable=False, unique=True, index=True)
    description = db.Column(db.String(500), nullable=True, default="")
    icon = db.Column(db.String(100), nullable=True, default="")

    def __str__(self):
        return self.name

    def __repr__(self):
        return '<Node: %s>' % self.name

    @classmethod
    def cached_node_list(cls):
        list = cache.get("node-list")
        if list:
            return list
        nodes = []
        for node in cls.query.all():
            nodes.append((node.id, node.name))
        cache.set("node-list", nodes)
        return nodes


def _clear_cache(sender, changes):
    for model, operation in changes:
        if isinstance(model, Node):
            cache.delete('node-list')


models_committed.connect(_clear_cache)
