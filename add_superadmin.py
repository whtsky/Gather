#!/usr/bin/env python
#coding=utf-8

from __future__ import print_function
from handlers.account import username_check
import settings
import pymongo
import hashlib

db = pymongo.Connection(host=settings.mongodb_host,
    port=settings.mongodb_port)[settings.database_name]

username = email = ''

while True:
    username = raw_input('username:')
    if username_check.findall(username)[0] != username:
        print("This username is not valid")
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
password = hashlib.sha1(password+email).hexdigest()

db.members.find_one({
'name': username,
'name_lower': username.lower(),
'password': password,
'email': email,
'website': '',
'description': '',
'locale': 'zh_CN-CN',
'role': 3,
'block': [],
'star': [],
})

