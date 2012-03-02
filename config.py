#coding=utf-8

admin = ('whtsky','jybox','abreto')
dict(
            bbs_title=xhtml_escape(u'ОЋгЂКазг'),
            bbs_title_e=xhtml_escape(u'Jybox'),
            bbs_url=u'http://bbs.jybox.net',
            template_path=os.path.join(os.path.dirname(__file__), 'templates'),
            static_path=os.path.join(os.path.dirname(__file__), 'static'),
            xsrf_cookies=True,
            ui_modules={"Post": PostListModule,
                        "TagCloud": TagCloudModule,
                        "Edit":EditModule},
            cookie_secret='89f3hneifu29IY(!H@@IUFY#(FCINepifu2iY!HU!(FU@H',
            login_url='/login',
            debug=False,
            autoescape=None,
        )