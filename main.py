#!/usr/bin/env python
# coding=utf-8

import os
import tornado.httpserver
import tornado.ioloop
import tornado.locale
import tornado.options
import tornado.web
import urls

from tornado.options import define, options
from raven.contrib.tornado import AsyncSentryClient
from init_db import db

ROOT = os.path.abspath(os.path.dirname(__file__))

define('port', default=8888, help='run on the given port', type=int)
define('settings', default=os.path.join(ROOT, 'settings.py'),
       help='path to the settings file.', type=str)


class Application(tornado.web.Application):
    def __init__(self):
        settings = {'template_path': os.path.join(ROOT, "templates"),
                    'role': {1: 'Member',
                             2: 'Admin',
                             3: 'SuperAdmin',
                             5: 'Owner'}}
        execfile(options.settings, {}, settings)

        settings['host'] = settings['forum_url'].split('/')[2]

        if 'static_path' not in settings:
            settings['static_path'] = os.path.join(ROOT, "static")

        super(Application, self).__init__(urls.handlers,
                                          ui_modules=urls.ui_modules, login_url='/account/signin',
                                          xsrf_cookies=True,
                                          **settings)

        self.db = db

        tornado.locale.load_translations(os.path.join(ROOT, "locale"))
        tornado.locale.set_default_locale(settings['default_locale'])
        supported_locales = list(tornado.locale.get_supported_locales())
        supported_locales.sort()
        locales = []
        for locale in supported_locales:
            locale = (locale, tornado.locale.LOCALE_NAMES[locale]['name'])
            locales.append(locale)
        self.locales = tuple(locales)
        
        self.sentry_client = AsyncSentryClient(settings['sentry_dsn'])


def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application(), xheaders=True)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()
