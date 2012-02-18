#coding=utf-8
import pymongo
db=pymongo.Connection().bbs
db.posts.drop()
db.users.drop()
db.tags.drop()
db.settings.drop()
import init