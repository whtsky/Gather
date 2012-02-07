#coding=utf-8
import pymongo
db=pymongo.Connection(host='127.0.0.1',port=27017).bbs
db.posts.save({'post_id':0})
db.posts.create_index([('changedtime',1)])
db.nodes.create_index([('_id',0)])
