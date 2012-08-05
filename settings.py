#coding=utf-8

mongodb_host = '127.0.0.1'
mongodb_port = 27017
database_name = 'forum'


forum_title = 'site_name'
forum_url = 'http://xxx.com/'
# forum_url MUST ends with '/'
only_use_forum_url = True
#Will redirect all the request to the forum url if True.
#static_path = ''
#static_url_prefix = 'http://assets.xxx.com'

default_locale = 'zh_CN'
notifications_per_page = 10
members_per_page = 100
topics_per_page = 20
replies_per_page = topics_per_page

gravatar_base_url = 'http://cn.gravatar.com/avatar/'
google_analytics = ''
cookie_secret = 'hey reset me!'

use_recaptcha = False  # If you use it,set to True
recaptcha_key = ''
recaptcha_secret = ''
recaptcha_theme = 'clean'

gzip = False
debug = True
