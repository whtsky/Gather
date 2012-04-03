#coding=utf-8
from tornado.escape import xhtml_escape

from common import BaseHandler,time_span
from config import admin

class RemoveUserHandler(BaseHandler):
    def get(self,username):
        assert self.get_current_user()['username'] in admin
        self.db.users.remove({'username':username})
        removepost(fliter={'author':username},db=self.db,mc=self.mc)
        postids = []
        for post in self.db.posts.find({'comments.author':username}):
            postids.append(post['_id'])
        self.db.posts.update({'comments.author':username},
                {'$pull':{'comments':{'author':username}}},multi=True)
        try:
            del self.mc['index']
            for postid in postids:
                del self.mc[str(postid)]
        except KeyError:
            pass
        self.redirect('/')

class RemovePostHandler(BaseHandler):
    def get(self,postid):
        assert self.get_current_user()['username'] in admin
        postid = int(postid)
        removepost(fliter={'_id':postid},db=self.db,mc=self.mc)
        try:
            del self.mc['index']
        except KeyError:
            pass
        self.redirect('/')

class RemoveCommentHandler(BaseHandler):
    def get(self,postid,commentid):
        assert self.get_current_user()['username'] in admin
        post = self.db.posts.find_one({'_id':int(postid)})
        del post['comments'][int(commentid)-1]
        self.db.posts.save(post)
        try:
            del self.mc['index']
        except KeyError:
            pass
        try:
            cache = self.mc[str(postid)]
        except KeyError:
            pass
        else:
            for i in range(len(post['comments'])):
                post['comments'][i]['location'] =  str(i+1)
            cache[2] = self.render_string('modules/comments.html',db=self.db,time_span=time_span,post=post)
            self.mc[str(postid)] = cache
        self.redirect('/topics/%s' % postid)


class ChangeTagHandler(BaseHandler):
    def post(self,postid):
        assert self.get_current_user()['username'] in admin
        postid = int(postid)
        post = self.db.posts.find_one({'_id':postid})
        for tag in post['tags']:
            self.db.tags.update({'name':tag},{'$inc':{'count':-1}})
        tags = []
        for x in xhtml_escape(self.get_argument('tags').lower()).split(' '):
            if x:
                tags.append(x)
        assert tags
        for tag in tags:
            self.db.tags.update({'name':tag},
                        {'$inc':{'count':1}},True)
        post['tags'] = tags
        self.db.posts.save(post)
        try:
            del self.mc['index']
            del self.mc['tagcloud:10']
            del self.mc['tagcloud:False']
        except KeyError:
            pass
        try:
            cache = self.mc[str(postid)]
        except KeyError:
            pass
        else:
            cache[0] = post
            self.mc[str(postid)] = cache
        self.redirect('/topics/'+str(postid))
        
def removepost(fliter,db,mc):
    for post in db.posts.find(fliter):
        db.users.update({'postmark':post['_id']},
                {'$pull':{'postmark':post['_id']}},multi=True)
        db.users.update({'notification.postid':post['_id']},{'$pull':{'notification':{'postid':post['_id']}}},multi=True)
        for tag in post['tags']:
            db.tags.update({'name':tag},{'$inc':{'count':-1}})
        try:
            del mc[str(post['_id'])]
        except KeyError:
            pass
    db.posts.remove(fliter)
    try:
        del mc['tagcloud:10']
        del mc['tagcloud:False']
    except KeyError:
        pass