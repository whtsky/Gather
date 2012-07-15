#!/usr/bin/env python
#coding=utf-8

import os
import tornado.httpserver
import tornado.ioloop
import tornado.locale
import tornado.options
import tornado.web
import pymongo
from tornado.options import define, options
import urls

define('port', default=8888, help='run on the given port', type=int)

ROOT = os.path.abspath(os.path.dirname(__file__))


class Application(tornado.web.Application):
    def __init__(self):
        settings = {'template_path': os.path.join(ROOT, "templates")}
        execfile('settings.py', {}, settings)

        if 'static_path' not in settings:
            settings['static_path'] = os.path.join(ROOT, "static")

        super(Application, self).__init__(urls.handlers,
            ui_modules=urls.ui_modules, login_url='/account/signin',
            **settings)

        self.db = pymongo.Connection(host=settings['mongodb_host'],
            port=settings['mongodb_port'])[settings['database_name']]

        tornado.locale.load_translations(os.path.join(ROOT, "locale"))
        tornado.locale.set_default_locale('zh_CN')


def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()
