# -*- coding:utf-8 -*-
import logging
from tornado.gen import coroutine
from wechat import WeiXinRequstHandler

__author__ = 'george'
"""
= 负责处理pdm室相关的业务
=
=

"""
class InstallTrayHandler(WeiXinRequstHandler):
    """安装托盘任务提交"""
    @coroutine
    def get(self, *args, **kwargs):

        self.render('ds/trayapply.html',code="23423432432432")

    @coroutine
    def post(self, *args, **kwargs):
        logging.info(self.request.body)
        #1 check提交的用户是否合法
        #超级表单

        #2 根据提交内容，发送图文消息给指定的用户

        pass

route=[
    (r'/ds/installtray',InstallTrayHandler)
]
