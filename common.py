#coding=utf-8

import tornado.web
import time
from markdown import Markdown
import re
from tornado.escape import xhtml_escape
from emoji import emojis
from config import google_analytics,admin

html_killer = re.compile('<[^>]*>')

#https://github.com/lepture/june/blob/master/june/lib/filters.py
url_replace = re.compile(r'(?m)^((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}'
                         r'/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+'
                         r'|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’]))')
pattern = re.compile(
    r'(?i)(?:&lt;)((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}'
    r'/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+'
    r'|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’]))(?:&gt;)')

youtube = re.compile('http://youtu.be/([a-zA-Z0-9\-\_]+)')
youku = re.compile('http://v.youku.com/v_show/id_([a-zA-Z0-9\=]+).html')
yinyuetai = re.compile('http://www.yinyuetai.com/video/(\d+)')
username_finder = re.compile(u'@(\w{1,25})\s')
emoji_finder = re.compile(u'(:[^:]+:)')

md = Markdown(extensions=['fenced_code','smart_strong','tables'])

class BaseHandler(tornado.web.RequestHandler):

    def __init__(self,*args,**kwargs):
        tornado.web.RequestHandler.__init__(self,*args,**kwargs)
        #方便调用
        self.db = self.application.db
        self.mc = self.application.mc

    def get_current_user(self):
        password = self.get_cookie('user')
        if password:
            return self.db.users.find_one({'password':password})
        else:
            return None

    def get_error_html(self,status_code, **kwargs):
        return self.render_string('404.html',google_analytics=google_analytics,admin_list=admin)

    def set_cookie(self, name, value, domain=None, expires=None, path="/",
                   expires_days=None, **kwargs):
        if not expires_days:
            expires_days = 365
        tornado.web.RequestHandler.set_cookie(self, name, value, domain, expires, path,
            expires_days, **kwargs)

    def render(self, template_name, **kwargs):
        user = self.get_current_user()
        unread = 0
        if user:
            for x in user['notification']:
                if not x['read']:
                    unread += 1
        tornado.web.RequestHandler.render(self,template_name=template_name,admin_list=admin,db=self.db,unread=unread,mc=self.mc,google_analytics=google_analytics,**kwargs)

class HomeHandler(BaseHandler):
    def get(self):
        posts = self.db.posts.find({},sort=[('changedtime', -1)],limit=15)
        self.render('index.html',time_span=time_span,posts=posts)

class EditModule(tornado.web.UIModule):
    def render(self,db):
        return self.render_string('modules/markdown.html',db=db)

class FeedHandler(BaseHandler):
    def get(self):
        self.set_header("Content-Type", "application/atom+xml")
        url = ''
        posts = [_ for _ in self.db.posts.find({},sort=[('changedtime', -1)],limit=20)]
        tornado.web.RequestHandler.render(self,'atom.xml',url=url,name='全站',
            time=time,posts=posts)

class ErrorHandler(BaseHandler):
    def get(self, *args, **kwargs):
        raise tornado.web.HTTPError(404)

def time_span(t):
    t=time.gmtime(t)
    return '<time datetime="%s" title="%s"></time>' % (time.strftime('%Y-%m-%dT%H:%M:%SZ',t),time.strftime('%Y年%m月%d日%H点%M分',t))

def md_convert(txt,notice=False,time=None,user=None,db=None,postid=None):
    #滤去html标签
    for x in set(html_killer.findall(txt)):
        txt = txt.replace(x,xhtml_escape(x))

    #https://github.com/livid/v2ex/blob/master/v2ex/templatetags/filters.py
    #视频支持
    for video_id in set(youtube.findall(txt)):
        txt = txt.replace('http://www.youtube.com/watch?v=' + video_id,'<object width="620" height="500"><param name="movie" value="http://www.youtube.com/v/' + video_id + '?fs=1&amp;hl=en_US"></param><param name="allowFullScreen" value="true"></param><param name="allowscriptaccess" value="always"></param><embed src="http://www.youtube.com/v/' + video_id + '?fs=1&amp;hl=en_US" type="application/x-shockwave-flash" allowscriptaccess="always" allowfullscreen="true" width="620" height="500"></embed></object>')
    for video_id in set(youku.findall(txt)):
        txt = txt.replace('http://v.youku.com/v_show/id_' + video_id + '.html', '<embed src="http://player.youku.com/player.php/sid/' + video_id + '/v.swf" quality="high" width="620" height="500" align="middle" allowScriptAccess="sameDomain" type="application/x-shockwave-flash"></embed>')
    for video_id in set(yinyuetai.findall(txt)):
        txt = txt.replace('http://www.yinyuetai.com/video/' + video_id,'<embed src="http://player.yinyuetai.com/video/player/354677/v_0.swf" quality="high" width="480" height="334" align="middle" allowScriptAccess="sameDomain" type="application/x-shockwave-flash"></embed>')

    txt = url_replace.sub(make_link,txt)
    txt = pattern.sub(make_link, txt)

    mentions = []
    for u in set(username_finder.findall(txt + ' ')):
        mentions.append(u)
        txt = txt.replace(u'@'+u,u'<a href="/user/%s">@%s</a>' % (u,u))

    for emoji in set(emoji_finder.findall(txt)):
        if emoji in emojis:
            txt = txt.replace(emoji,u'<img src="/static/img/%s" class="emoji" />' % emojis[emoji])

    txt = md.convert(txt).replace('\n','<br />')

    if notice:
        for u in mentions:
            db.users.update({'username':u},
            {'$push':
                     {'notification':
                              {'from':user,
                               'content':txt,
                               'time':time,
                               'postid':postid,
                               'read':False,
                               }
                     },
            })

    return txt

def make_link(m):
    link = m.group(1)
    if link.startswith('https://gist.github.com/') or link.startswith('http://gist.github.com/'):
        return '<script src="%s.js"></script>' % link.replace('https','http')
    if '.jpg' in link or '.jpeg' in link or '.gif' in link or '.png' in link:
        return '<img src="%s" />' % link
    else:
        return '<a href="%s" rel="nofollow" target="_blank">%s</a>' % (link, link)