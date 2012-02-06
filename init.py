import pymongo
db=pymongo.Connection(host='127.0.0.1',port=27017).bbs
db.posts.save({'post_id':0})
#TODO:创建以时间为主键的索引