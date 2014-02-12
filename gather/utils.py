# -*- coding:utf-8 -*-
import functools

from flask import current_app, request, abort
from gather.extensions import mail


def send_mail(msg):
    if current_app.debug:
        print msg.html
    else:
        mail.send(msg)


def get_page():
    try:
        page = int(request.args.get('page', 1))
    except ValueError:
        abort(404)
    else:
        if page:
            return page
    abort(404)


def no_xhr(method):
    @functools.wraps(method)
    def wrapper(*args, **kwargs):
        if request.is_xhr:
            return abort(403)
        return method(*args, **kwargs)

    return wrapper
