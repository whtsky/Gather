#coding=utf-8
import os

admin = ('whtsky','jybox','abreto')
settings = dict(
    bbs_title=u'精英盒子',
    bbs_title_e=u'Jybox',
    bbs_url=u'http://bbs.jybox.net',
    template_path=os.path.join(os.path.dirname(__file__), 'templates'),
    static_path=os.path.join(os.path.dirname(__file__), 'static'),
    xsrf_cookies=True,
    cookie_secret='89f3hneifu29IY(!H@@IUFY#(FCINepifu2iY!HU!(FU@H',
    login_url='/login',
    debug=False,
    autoescape=None,
)