#coding=utf-8

from . import BaseHandler


class UserAgentHandler(BaseHandler):
	def get(self):
		ua = self.request.headers.get("User-Agent", "Unknow")
		source = self.get_source()
		if not source:
			source = 'Desktop'
		self.render('others/ua.html', ua=ua, source=source)
		
handlers = [
	(r'/ua', UserAgentHandler),
]
