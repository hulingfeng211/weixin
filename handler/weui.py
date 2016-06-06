# -*- conding:utf -*- 
#===================================================
#	creater:george
#	email:hulingfeng211@163.com
#	create time:2016-06-06 15:07
#	description:
#
#===================================================

from tornado.web import RequestHandler,url

class IndexHandler(RequestHandler):
	def get(self,*args,**kwargs):
		self.render('weui/index.html')
		pass

class Index2Handler(RequestHandler):
	def get(self,*args,**kwargs):
		self.render('weui/jquery-weui-demos/index.html')

class PageHandler(RequestHandler):
	#(r"/(P?<nickname>.*)/article/details/(P?<postid>.*)", MainHandler),
	def get(self,*args):
		#self.write(args[0])
		self.render('weui/jquery-weui-demos/%s'%args[0])





routes = [
	url(r'/weui',IndexHandler,name='weui.home'),
	url(r'/weui2',Index2Handler),
	url(r'/(.*)',PageHandler), # 

	
]