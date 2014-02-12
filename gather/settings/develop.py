# -*- coding:utf-8 -*-
import os

FORUM_DOMAIN = "127.0.0.1"
FORUM_URL = "http://%s" % FORUM_DOMAIN
DEFAULT_MAIL_SENDER = "no-reply@%s" % FORUM_DOMAIN

DEBUG = True

CACHE_TYPE = "memcached"
CACHE_KEY_PREFIX = "gather_"
SECRET_KEY = "develop"

SQLALCHEMY_DATABASE_URI = 'sqlite:///%s' % os.path.join(
    os.getcwd(), 'db.sqlite'
)

PASSWORD_SECRET = "develop"
