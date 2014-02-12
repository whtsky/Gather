# -*- coding:utf-8 -*-

from flask import Blueprint
from flask import url_for, g, redirect, render_template, abort
from gather.utils import get_page
from gather.account.utils import require_login, require_staff
from .forms import CreateTopicForm, ChangeTopicForm, ReplyForm, ChangeReplyForm
from .models import Topic, Reply

bp = Blueprint("topic", __name__, url_prefix="/topic")


@bp.route("/")
def index():
    page = get_page()
    paginator = Topic.query.order_by(Topic.updated.desc()).paginate(page)
    return render_template('topic/index.html', paginator=paginator)


@bp.route("/create", methods=("GET", "POST"))
@require_login
def create():
    form = CreateTopicForm()
    if form.validate_on_submit():
        topic = form.create()
        return redirect(url_for(".topic", topic_id=topic.id))
    return render_template("topic/create.html", form=form)


@bp.route("/<int:topic_id>", methods=("GET", "POST"))
def topic(topic_id):
    page = get_page()
    topic = Topic.query.get_or_404(topic_id)
    form = ReplyForm()
    if g.user and form.validate_on_submit():
        form.create(topic=topic)
        pages = Reply.query.filter_by(topic=topic).paginate(1).pages
        base_url = url_for(".topic", topic_id=topic.id)
        return redirect("%s?page=%s" % (base_url, pages))
    replies = Reply.query.filter_by(topic=topic).order_by(Reply.id.asc())
    paginator = replies.paginate(page, per_page=50)
    return render_template(
        "topic/topic.html", topic=topic, form=form,
        paginator=paginator
    )


@bp.route("/<int:topic_id>/change", methods=("GET", "POST"))
@require_staff
def change_topic(topic_id):
    topic = Topic.query.get_or_404(topic_id)
    form = ChangeTopicForm(obj=topic)
    if form.validate_on_submit():
        topic = form.save(topic=topic)
        return redirect(url_for(".topic", topic_id=topic.id))
    return render_template("topic/change.html", form=form)


@bp.route("/<int:topic_id>/<int:reply_id>/change", methods=("GET", "POST"))
@require_staff
def change_reply(topic_id, reply_id):
    topic = Topic.query.get_or_404(topic_id)
    reply = Reply.query.get_or_404(reply_id)
    if reply.topic != topic:
        abort(233)
    form = ChangeReplyForm(obj=reply)
    if form.validate_on_submit():
        form.save(reply=reply)
        return redirect(url_for(".topic", topic_id=topic.id))
    return render_template("topic/change_reply.html", form=form)