# -*- coding:utf-8 -*-

from flask import Blueprint, abort
from flask import request, url_for
from flask import g, render_template, redirect
from gather.account.forms import (LoginForm, RegisterForm,
                                  FindForm, ResetForm, SettingsForm)
from gather.account.utils import require_login, login_user, logout_user, verify_reset_token
from gather.utils import require_token

bp = Blueprint("account", __name__, url_prefix="/account")


@bp.route("/login", methods=("GET", "POST"))
def login():
    next_url = request.args.get('next', "/")
    form = LoginForm()
    if form.validate_on_submit():
        form.login()
        return redirect(next_url)
    return render_template("account/login.html", form=form)


@bp.route("/register", methods=("GET", "POST"))
def register():
    next_url = request.args.get('next', url_for('.settings'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = form.save()
        login_user(user)
        return redirect(next_url)
    return render_template("account/register.html", form=form)


@bp.route("/logout/<token>")
@require_login
@require_token
def logout():
    next_url = request.args.get('next', "/")
    logout_user()
    return redirect(next_url)


@bp.route("/find", methods=("GET", "POST"))
def find_password():
    if g.user:
        return redirect("/")
    form = FindForm()
    if form.validate_on_submit():
        form.send()
        return render_template("account/find_sent.html")
    return render_template("account/find_password.html", form=form)


@bp.route("/reset", methods=("GET", "POST"))
def reset():
    token = request.args.get("token", None)
    user = verify_reset_token(token)
    if not user:
        return abort(403)
    form = ResetForm()
    if form.validate_on_submit():
        user = form.reset(user)
        login_user(user)
        return redirect("/")
    return render_template("account/reset.html", form=form)


@bp.route("/settings", methods=("GET", "POST"))
@require_login
def settings():
    user = g.user
    form = SettingsForm(obj=user)
    next_url = request.args.get('next', url_for('.settings'))
    if form.validate_on_submit():
        form.save()
        return redirect(next_url)
    return render_template('account/settings.html', form=form)
