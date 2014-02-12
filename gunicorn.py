# -*- coding:utf-8 -*-

# workers = 4

import gevent.monkey
gevent.monkey.patch_all()

worker_class = 'gevent'
bind = "127.0.0.1:8000"
backlog = 2048

pidfile = "/tmp/gather.pid"
