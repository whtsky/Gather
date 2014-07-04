# -*- coding:utf-8 -*-

from flask import g, request
from flask.ext.restless import ProcessingException


EXCLUDE_COLUMNS = [
    "password", "token", "api_token",
    "author.password", "author.token", "author.api_token"
]


def need_auth(**kw):
    from gather.account.models import Account
    token = request.headers.get("token", None)
    user = None
    if token:
        user = Account.query.filter_by(api_token=token).first()
    if not user:
        raise ProcessingException(description='Not Authorized', code=401)
    g.token_user = user
