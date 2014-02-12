import os

gather_base_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))

FORUM_TITLE = "Gather"

FORUM_DOMAIN = "127.0.0.1"
FORUM_URL = "http://%s" % FORUM_DOMAIN
MAIL_DEFAULT_SENDER = "no-reply@%s" % FORUM_DOMAIN

PRODUCTION_USER = "gather"

GRAVATAR_BASE_URL = "http://cn.gravatar.com/avatar/"

CACHE_TYPE = "memcached"
CACHE_KEY_PREFIX = "gather_"

SQLALCHEMY_COMMIT_ON_TEARDOWN = True

ASSETS_LOAD_PATH = [os.path.join(gather_base_dir, "assets")]
DEBUG_TB_PROFILER_ENABLED = True
DEBUG_TB_TEMPLATE_EDITOR_ENABLED = True
