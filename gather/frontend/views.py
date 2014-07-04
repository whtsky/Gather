# -*- coding:utf-8 -*-

from flask import Blueprint, render_template, make_response

bp = Blueprint("frontend", __name__, url_prefix="")


@bp.route("/")
def index():
    from gather.topic.models import Topic
    topics = Topic.query.order_by(Topic.updated.desc()).limit(5)
    return render_template("index.html", topics=topics)


@bp.route("/feed")
def feed():
    from gather.topic.models import Topic
    topics = Topic.query.order_by(Topic.updated.desc()).limit(15)
    response = make_response(render_template("feed.xml", topics=topics))
    response.mimetype = "application/atom+xml"
    return response

