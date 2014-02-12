# -*- coding:utf-8 -*-

import multiprocessing

workers = multiprocessing.cpu_count() * 2 + 1

import gevent.monkey
gevent.monkey.patch_all()

worker_class = 'gevent'
bind = "127.0.0.1:8000"

pidfile = "/tmp/gather.pid"
