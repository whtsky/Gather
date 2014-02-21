# -*- coding:utf-8 -*-

from flask import Blueprint
from flask import render_template, redirect, url_for

from gather.account.utils import require_staff
from gather.topic.models import Topic
from .forms import CreateNodeForm, ChangeNodeForm
from .models import Node

bp = Blueprint("node", __name__, url_prefix="/node")


@bp.route("/")
def index():
    items = Node.query.all()
    return render_template("node/index.html", items=items)


@bp.route("/create", methods=("GET", "POST"))
@require_staff
def create():
    form = CreateNodeForm()
    if form.validate_on_submit():
        form.create()
        return redirect(url_for(".node", slug=form.node.slug))
    return render_template("node/create.html", form=form)


@bp.route("/<slug>", defaults={'page': 1})
@bp.route("/<slug>/page/<int:page>")
def node(slug, page):
    node = Node.query.filter_by(slug=slug).first_or_404()
    topics = Topic.query.filter_by(node=node)
    paginator = topics.order_by(Topic.updated.desc()).paginate(page)
    return render_template("node/node.html", node=node, paginator=paginator)


@bp.route("/<slug>/change", methods=("GET", "POST"))
def change(slug):
    node = Node.query.filter_by(slug=slug).first_or_404()
    form = ChangeNodeForm(obj=node)
    if form.validate_on_submit():
        form.save(node=node)
        return redirect(url_for(".node", slug=node.slug))
    return render_template("node/change.html", form=form)
