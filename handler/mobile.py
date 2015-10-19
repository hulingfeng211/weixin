#!/usr/bin/env python
# -*- coding:utf-8 -*- 
"""========================================================== 
|   FileName:mobile.py
|   Author: george
|   mail:hulingfeng211@163.com
|   Created Time:2015年10月19日 星期一 14时17分03秒
|   Description:与手机相关的请求在该模块下进行处理
+============================================================"""
from tornado.gen import coroutine
from tornado.web import RequestHandler
import constant
from urllib import quote, urlencode


class IndexHanlder(RequestHandler):

    @coroutine
    def get(self, *args, **kwargs):
        user_id=self.get_secure_cookie('userid')
        if user_id:
            self.write('userid')
        else:
            redirct_url=constant.BASE_URL+'/mobile/index.html'
            args={"CorpID":self.settings[constant.WEIXIN_SETTINGS][constant.CorpID],
                                              "redirect_uri":redirct_url}
            url=constant.QUERY_AUTH_CODE_URL%args
            self.write(url)
            #get
            pass

    @coroutine
    def post(self, *args, **kwargs):
        pass

route=[(r'/mobile/index.html',IndexHanlder),]


if __name__== "__main__":
    pass