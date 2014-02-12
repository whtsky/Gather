# -*- coding:utf-8 -*-

from flask.ext.restful import Resource
from gather.account.models import Account


class UserAPI(Resource):
    def get(self):
        users = []
        for user in Account.query.all():
            users.append({
                "username": user.username,
                "email": user.email,

            })