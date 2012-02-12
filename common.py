#coding=utf-8

import tornado.web
import time
from markdown import Markdown
import re
from tornado.escape import xhtml_escape

html_killer = re.compile('<[^>]*>')
url_replace = re.compile(u'[^\(]((?:HTTP|HTTPS|FTP|ED2K|THUNDER|FLASHGETX|http|https|ftp|ed2k|thunder|flashgetx)://[^\u4e00-\u9fa5 ]+)')
url_replace_2 = re.compile(u'((?:HTTP|HTTPS|FTP|ED2K|THUNDER|FLASHGETX|http|https|ftp|ed2k|thunder|flashgetx)://[^\u4e00-\u9fa5 ]+)[^\)]')
pure_url = re.compile(u'((?:HTTP|HTTPS|FTP|ED2K|THUNDER|FLASHGETX|http|https|ftp|ed2k|thunder|flashgetx)://[^\u4e00-\u9fa5 ]+)')
img_replace = re.compile(u'[^\(]((?:HTTP|HTTPS|http|https)://[^\u4e00-\u9fa5 ]+(?:.jpg|.jpeg|.gif|.png|.JPG|.JPEG|.GIF|.PNG))')
img_replace_2 = re.compile(u'((?:HTTP|HTTPS|http|https)://[^\u4e00-\u9fa5 ]+(?:.jpg|.jpeg|.gif|.png|.JPG|.JPEG|.GIF|.PNG))[^)]')
pure_img = re.compile(u'((?:HTTP|HTTPS|http|https)://[^\u4e00-\u9fa5 ]+(?:.jpg|.jpeg|.gif|.png|.JPG|.JPEG|.GIF|.PNG))')

md = Markdown(extensions=['fenced_code','smart_strong','tables'])

class BaseHandler(tornado.web.RequestHandler):

    def __init__(self,*args,**kwargs):
        tornado.web.RequestHandler.__init__(self,*args,**kwargs)
        #方便调用
        self.db = self.application.db

    def get_current_user(self):
        return self.get_secure_cookie('user')

def time_span(t):
    timecha = int(time.time()) - t
    if timecha < 60:
        return str(timecha)+u'秒前'
    elif timecha < 3600:
        return str(timecha/60)+u'分钟前'
    elif timecha < 86400:
        return str(timecha/3600)+u'小时前'
    elif timecha < 1296000:
        return str(timecha/86400)+u'天前'
    else:
        return time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(t+28800))

def md_convert(txt):
    #滤去html标签
    for x in set(html_killer.findall(txt)):
        txt = txt.replace(x,xhtml_escape(x))

    try:
        t = pure_img.findall(txt)[0]
        if t == txt:
            return md.convert(u'![%s](%s)' % (t,t))
    except:
        try:
            t = pure_url.findall(txt)[0]
            if t == txt:
                return md.convert(u'[%s](%s)' % (t,t))
        except:
            pass


    for x in set(img_replace.findall(txt)):
        txt = txt.replace(x,u'![%s](%s)' % (x,x))
    for x in set(img_replace_2.findall(txt)):
        txt = txt.replace(x,u'![%s](%s)' % (x,x))
    for x in set(url_replace.findall(txt)):
        txt = txt.replace(x,u'[%s](%s)' % (x,x))
    for x in set(url_replace_2.findall(txt)):
        txt = txt.replace(x,u'[%s](%s)' % (x,x))

    return xhtml_escape(md.convert(txt))

def getvalue(dict,keyname):
    try:
        return dict[keyname]
    except:
        return ''