#!/usr/bin/env python
#coding=utf-8

import settings
import pymongo

db = pymongo.Connection(host=settings.mongodb_host,
    port=settings.mongodb_port)[settings.database_name]
db.members.create_index([('created', 1)])
db.topics.create_index([('last_reply_time', -1), ('node', 1)])
db.replies.create_index([('topic', 1), ('index', 1)])
db.notifications.create_index([('to', 1), ('created', 1)])
