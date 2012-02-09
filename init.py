#coding=utf-8
import pymongo
db=pymongo.Connection(host='127.0.0.1',port=27017).bbs
db.settings.save({'post_id':0})
db.settings.save({'node_id':0})
db.settings.insert({'name':'tag-count'})
db.posts.create_index([('changedtime',1)])