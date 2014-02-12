# -*- coding:utf-8 -*-

import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))


def load_develop_settings(app):
    app.config.from_pyfile(os.path.join(BASEDIR, "develop.py"))


def load_production_settings(app):
    app.config.from_pyfile(os.path.join(BASEDIR, "production.py"))


def load_settings(app):
    app.config.from_pyfile(os.path.join(BASEDIR, "base.py"))
    load_develop_settings(app)
    import getpass
    if getpass.getuser() == app.config["PRODUCTION_USER"]:
        load_production_settings(app)
