# -*- coding:utf-8 -*-

from flask import g, request
from flask.ext.restless import ProcessingException


EXCLUDE_COLUMNS = [
    "password", "token", "api_token",
    "author.password", "author.token", "author.api_token"
]


def need_auth(**kw):
    if not g.token_user:
        raise ProcessingException(description='Not Authorized', code=401)
