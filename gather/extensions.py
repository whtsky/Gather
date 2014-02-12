# -*- coding:utf-8 -*-

__all__ = ["db", "assets"]

from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.assets import Environment, Bundle
from flask.ext.mail import Mail
from flask.ext.cache import Cache

db = SQLAlchemy()
assets = Environment()

js_all = Bundle(
    "javascripts/libs/jquery-2.1.0.min.js",
    "javascripts/libs/turbolinks.js",
    "javascripts/libs/jquery.atwho.js",
    Bundle(
        "javascripts/libs/timeago.coffee",
        "javascripts/libs/locales/timeago.zh-cn.coffee",
        "javascripts/turbolinks_icon.coffee",
        "javascripts/gather.coffee",
        filters="coffeescript"
    ),
    filters="rjsmin",
    output="gather.js"
)
assets.register("js_all", js_all)

css_all = Bundle(
    "stylesheets/gather.sass",
    depends=["stylesheets/*.sass", "stylesheets/*.scss"],
    filters=("sass", "cssmin"),
    output="gather.css"
)
assets.register("css_all", css_all)

mail = Mail()
cache = Cache()
