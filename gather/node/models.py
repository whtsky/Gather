# -*- coding:utf-8 -*-

from __future__ import unicode_literals

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
    def query_all(cls):
        return cls.query.order_by(Node.name.asc()).all()

    def to_dict(self):
        return dict(
            id=self.id,
            name=self.name,
            slug=self.slug,
            description=self.description,
            icon=self.icon
        )

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        from gather.topic.models import Topic
        for topic in Topic.query.filter_by(node=self).all():
            topic.delete()
        db.session.delete(self)
        db.session.commit()
        return self
