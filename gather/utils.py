# -*- coding:utf-8 -*-
import functools

from flask import current_app, request, abort
from gather.extensions import mail


def send_mail(msg):
    if current_app.debug:
        print msg.html
    else:
        mail.send(msg)


def no_xhr(method):
    @functools.wraps(method)
    def wrapper(*args, **kwargs):
        if request.is_xhr:
            return abort(403)
        return method(*args, **kwargs)

    return wrapper
