# -*- coding:utf-8 -*-

import functools
import time
import hashlib
import base64

from flask import current_app
from flask import g, request, session
from flask import url_for, redirect, abort

from gather.account.models import Account, ROLES


class RequireRole(object):
    def __init__(self, role):
        self.role = role

    def __call__(self, method):
        @functools.wraps(method)
        def wrapper(*args, **kwargs):
            if not g.user:
                url = url_for("account.login")
                if "?" not in url:
                    url += "?next=" + request.url
                return redirect(url)
            if self.role is None:
                return method(*args, **kwargs)
            if g.user.id == 1:
                return method(*args, **kwargs)
            if ROLES[g.user.role] < ROLES[self.role]:
                return abort(403)
            return method(*args, **kwargs)
        return wrapper


require_login = RequireRole("user")
require_staff = RequireRole("staff")
require_admin = RequireRole("admin")


def get_current_user():
    if "id" in session and "token" in session:
        user = Account.query.get(int(session["id"]))
        if not user:
            return None
        if user.token != session["token"]:
            return None
        return user
    return None


def login_user(user, permanent=True):
    if not user:
        return None
    session["id"] = user.id
    session["token"] = user.token
    if permanent:
        session.permanent = True
    return user


def logout_user():
    if "id" not in session:
        return
    session.pop("id")
    session.pop("token")


def create_reset_token(user):
    timestamp = str(int(time.time()))
    user_id = str(user.id)
    token = "|".join([user_id, timestamp, current_app.secret_key])
    hsh = hashlib.sha512(token).hexdigest()
    return base64.b64encode("|".join([timestamp, user_id, hsh]))


def verify_reset_token(token):
    try:
        timestamp, user_id, hsh = base64.b64decode(token).split("|")
    except Exception:
        return
    token = "|".join([user_id, timestamp, current_app.secret_key])
    if hsh != hashlib.sha512(token).hexdigest():
        return
    return Account.query.get(int(user_id))
