
import re
import time
from tornado.escape import xhtml_escape, _unicode, _URL_RE
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name, TextLexer

username_validator = re.compile(r'^[a-zA-Z0-9]+$')
email_validator = re.compile(r'^.+@[^.].*\.[a-z]{2,10}$', re.IGNORECASE)

_GIST_RE = re.compile(r'(https?://gist.github.com/[\d]+)')
_CODE_RE = re.compile(r'```(\w+)(.+?)```', re.S)

formatter = HtmlFormatter()


def utc_time():
    return int(time.mktime(time.gmtime()))


def make_content(text, extra_params='rel="nofollow"'):
    """https://github.com/facebook/tornado/blob/master/tornado/escape.py#L238
    """
    if extra_params:
        extra_params = " " + extra_params.strip()

    def make_link(m):
        url = m.group(1)
        proto = m.group(2)

        href = m.group(1)
        if not proto:
            href = "http://" + href   # no proto specified, use http

        params = extra_params

        match = _GIST_RE.match(href)
        if match:
            return '<script src="%s.js"></script>' % match.group(1)

        if '.' in href:
            name_extension = href.split('.')[-1]
            if name_extension in ('jpg', 'png', 'git', 'jpeg'):
                return u'<img src="%s" />' % href

        return u'<a href="%s"%s>%s</a>' % (href, params, url)

    def highligt(m):
        try:
            name = m.group(1)
            lexer = get_lexer_by_name(name)
        except ValueError:
            lexer = TextLexer()
        text = m.group(2).replace('&quot;', '"').replace('&amp;', '&')
        text = text.replace('&lt;', '<').replace('&gt;', '>')
        return highlight(text, lexer, formatter)

    text = _unicode(xhtml_escape(text))
    text = _CODE_RE.sub(highligt, text).replace('\n', '<br />')
    return _URL_RE.sub(make_link, text)
