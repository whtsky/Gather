# -*- coding:utf-8 -*-

from flask import Blueprint, redirect, url_for
from flask import render_template, request

from gather.utils import no_xhr
from gather.account.models import db, Account
from gather.account.utils import require_admin
from gather.topic.models import Topic

bp = Blueprint("user", __name__, url_prefix="/user")


@bp.route("/", defaults={'page': 1})
@bp.route('/page/<int:page>')
def index(page):
    accounts = Account.query.order_by(Account.id.desc())
    paginator = accounts.paginate(page, per_page=18)
    return render_template("user/index.html", paginator=paginator)


@bp.route("/<name>")
def profile(name):
    user = Account.query.filter_by(username=name).first_or_404()
    topics = Topic.query.filter_by(author=user).order_by(Topic.id.desc())[:5]
    return render_template("user/profile.html", user=user, topics=topics)


@bp.route("/<name>/topic", defaults={'page': 1})
@bp.route('/<name>/topic/page/<int:page>')
def topic(name, page):
    user = Account.query.filter_by(username=name).first_or_404()
    paginator = Topic.query.filter_by(author=user).\
        order_by(Topic.created.desc()).paginate(page)
    return render_template('user/topic.html', user=user, paginator=paginator)


@bp.route("/<name>/promote")
@no_xhr
@require_admin
def promote(name):
    user = Account.query.filter_by(username=name).first_or_404()
    user.role = "staff"
    db.session.add(user)
    db.session.commit()
    return redirect(url_for(".profile", name=user.username))


@bp.route("/<name>/demote")
@no_xhr
@require_admin
def demote(name):
    user = Account.query.filter_by(username=name).first_or_404()
    user.role = "user"
    db.session.add(user)
    db.session.commit()
    return redirect(url_for(".profile", name=user.username))