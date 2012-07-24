#!/usr/bin/env python
#coding=utf-8

from __future__ import print_function
import time
import settings
from handlers.utils import username_validator
import hashlib

import pymongo

db = pymongo.Connection(host=settings.mongodb_host,
    port=settings.mongodb_port)[settings.database_name]
db.members.create_index([('created', -1)])
db.topics.create_index([('last_reply_time', -1), ('node', 1)])
db.replies.create_index([('topic', 1), ('index', 1)])
db.notifications.create_index([('to', 1), ('created', 1)])
db.links.create_index([('priority', -1)])


if __name__ == '__main__':

    username = email = ''

    while True:
        username = raw_input('username:')
        if not username_validator.match(username):
            print("Invalid username")
            continue
        if not db.members.find_one({'name_lower': username.lower()}):
            break
        else:
            print("This username is already registered")

    while True:
        email = raw_input('email:').lower()
        if not db.members.find_one({'email': email}):
            break
        print("This email is already registered")

    password = raw_input('password:')
    password = hashlib.sha1(password + username.lower()).hexdigest()

    db.members.insert({
    'name': username,
    'name_lower': username.lower(),
    'password': password,
    'email': email,
    'website': '',
    'description': '',
    'created': time.time(),
    'role': 3,
    'language': settings.default_locale,
    'block': [],
    'like': [],  # topics
    'follow': [],  # users
    'favorite': []  # nodes
    })
