# -*- coding:utf-8 -*-

from __future__ import unicode_literals

from flask import g
from flask.ext.wtf import Form as _Form
from flask.ext.wtf.csrf import generate_csrf, validate_csrf
from wtforms import ValidationError
from gather.extensions import cache


class Form(_Form):
    """
    让 CSRF 成为基于 Cache 的一次性字符
    """

    def generate_csrf_token(self, csrf_context=None):
        if not self.csrf_enabled:
            return None
        csrf = generate_csrf(self.SECRET_KEY, self.TIME_LIMIT)
        if g.user:
            cache_value = g.user.id
        else:
            cache_value = 0
        cache.set(csrf, cache_value, self.TIME_LIMIT)
        return csrf

    def validate_csrf_token(self, field):
        if not self.csrf_enabled:
            return True
        if not self.validate_csrf_data(field.data):
            raise ValidationError("Wrong CSRF Token")

    def validate_csrf_data(self, data):
        if not validate_csrf(data, self.SECRET_KEY, self.TIME_LIMIT):
            return False
        cache_value = cache.get(data)
        cache.delete(data)
        if cache_value is not None:
            if cache_value == 0:
                return True
            return cache_value == g.user.id
        return False
