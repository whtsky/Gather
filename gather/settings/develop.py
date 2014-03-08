# -*- coding:utf-8 -*-
import os

DEBUG = True

SECRET_KEY = "develop"

"""
SQLALCHEMY_DATABASE_URI = 'sqlite:///%s' % os.path.join(
    os.getcwd(), 'db.sqlite'
)
"""

SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://postgres@localhost/gather"


PASSWORD_SECRET = "develop"

CACHE_TYPE = "simple"
