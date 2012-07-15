#!/usr/bin/env python
#coding=utf-8

import settings
import pymongo

db = pymongo.Connection(host=settings.mongodb_host,
    port=settings.mongodb_port)[settings.database_name]
db.topics.create_index([('modified', 1), ('node', 1)])
db.replies.create_index([('topic', 1), ('index', -1)])
