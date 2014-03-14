# -*- coding:utf-8 -*-

import functools

from flask import current_app, request, abort, g
from werkzeug.security import gen_salt
from gather.extensions import mail, cache


def send_mail(msg):
    if current_app.debug:
        print msg.html
    else:
        mail.send(msg)


def gen_action_token(length=40):
    if not g.user:
        return
    user = g.user
    token = gen_salt(length=length)
    cache.set("action_token_{}".format(token), user.id, timeout=300)
    return token


def verify_action_token(token):
    if not g.user:
        return False
    user = g.user
    key = "action_token_{}".format(token)
    user_id = cache.get(key)
    if user_id:
        cache.delete(key)
        return user_id == user.id
    return False


def require_token(method):
    @functools.wraps(method)
    def wrapper(*args, **kwargs):
        token = kwargs.pop("token", "")
        if not verify_action_token(token):
            return abort(403)
        return method(*args, **kwargs)

    return wrapper