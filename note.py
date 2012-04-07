#coding=utf-8
from common import BaseHandler,md_convert,time_span
from tornado.web import authenticated
from tornado.web import HTTPError
from time import time

class NoteHandler(BaseHandler):
    @authenticated
    def get(self):
        notes = self.db.notes.find({'author':self.current_user['username']},sort=[('changedtime', -1)])
        self.render('notes.html',time_span=time_span,notes=notes)

class NoteEditHandler(BaseHandler):
    @authenticated
    def get(self,key):
        note = self.db.notes.find_one({'posttime':int(key),'author':self.current_user['username']})
        self.render('made.html',title=note['title'],note_id=note['posttime'])

class NoteRawHandler(BaseHandler):
    @authenticated
    def get(self,key):
        note = self.db.notes.find_one({'posttime':int(key),'author':self.current_user['username']})
        if note:
            self.write(note['md'])
        else:
            raise HTTPError(404)

    @authenticated
    def post(self,key):
        md = self.get_argument('md','')
        note = self.db.notes.find_one({'posttime':int(key),'author':self.current_user['username']})
        if note['md'] != md:
            note['md'] = md
            self.db.notes.save(note)
        self.write(md_convert(md))

class NoteAddHandler(BaseHandler):
    @authenticated
    def get(self):
        user = self.current_user
        current_time = int(time())
        self.db.notes.insert({'title':self.get_argument('title'),'posttime':current_time,
                              'author':user['username'],'changedtime':current_time,'md':''})
        self.redirect('/notes/edit/%s' % current_time)

class NoteRemoveHandler(BaseHandler):
    @authenticated
    def get(self,key):
        self.db.notes.remove({'posttime':int(key),'author':self.current_user['username']})
        self.redirect('/notes')

class NoteRenameHandler(BaseHandler):
    @authenticated
    def post(self,key):
        note = self.db.notes.find_one({'posttime':int(key),'author':self.current_user['username']})
        title = self.get_argument('title')
        if note['title'] != title:
            note['title'] = title
            self.db.notes.save(note)
        self.redirect('/notes')

class NotePublishHandler(BaseHandler):
    @authenticated
    def get(self,key):
        note = self.db.notes.find_one({'posttime':int(key),'author':self.current_user['username']})
        if note:
            self.render('note_publish.html',title=note['title'],content=note['md'])
        else:
            raise HTTPError(404)
