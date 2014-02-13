# -*- coding:utf-8 -*-
import os

DEBUG = True

SECRET_KEY = "develop"

SQLALCHEMY_DATABASE_URI = 'sqlite:///%s' % os.path.join(
    os.getcwd(), 'db.sqlite'
)

PASSWORD_SECRET = "develop"
