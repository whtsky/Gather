# -*- coding:utf-8 -*-

from flask import Blueprint, abort, jsonify
from flask import request, url_for, g
from gather.extensions import cache
from gather.utils import get_page
from gather.account.models import db, Account
from gather.node.models import Node
from gather.topic.models import Topic


bp = Blueprint("api", __name__, url_prefix="/api")


@bp.route("/user", methods=("GET", "POST"))
def users():
    if request.method == "GET":
        page = get_page()
        users = Account.query.order_by(Account.id.desc())
    elif request.method == "POST":
        pass


@bp.route("/user/<int:uid>", methods=("GET", "PUT"))
def user(uid):
    user = Account.query.get_or_404(uid)
    if request.method == "GET":
        return jsonify(user=user.to_dict())


@bp.route("/topic", methods=("GET", "POST"))
def topics():
    if request.method == "GET":
        page = get_page()
        topics = Topic.query.order_by(Topic.id.desc())
    elif request.method == "POST":
        pass


@bp.route("/topic/<int:uid>", methods=("GET", "PUT"))
def topic(uid):
    topic = Topic.query.get_or_404(uid)
    if request.method == "GET":
        return jsonify(topic=topic.to_dict())
    elif request.method == "POST":
        pass


@bp.route("/topic/<int:uid>/reply", methods=("GET", "POST"))
def replies(uid):
    topic = Topic.query.get_or_404(uid)
    if request.method == "GET":
        return jsonify(topic=topic.to_dict())
    elif request.method == "POST":
        pass


@bp.route("/node", methods=("GET", "POST"))
def nodes():
    if request.method == "GET":
        page = get_page()
        nodes = Node.query.order_by(Node.id.desc())
    elif request.method == "POST":
        pass


@bp.route("/node/<int:uid>", methods=("GET", "PUT"))
def node(uid):
    node = Node.query.get_or_404(uid)
    if request.method == "GET":
        return jsonify(node=node.to_dict())
