#!/usr/bin/env python
# -*- coding:utf-8 -*- 
"""========================================================== 
|   FileName:mobile.py
|   Author: george
|   mail:hulingfeng211@163.com
|   Created Time:2015年10月19日 星期一 14时17分03秒
|   Description:与手机相关的请求在该模块下进行处理
+============================================================"""
import json
from tornado import escape

from tornado.gen import coroutine, Return
from tornado.web import RequestHandler
from torndsession.sessionhandler import SessionBaseHandler
from urllib import quote, urlencode
import constant
from core.utils import send_request
from wechat import get_access_token


class BaseHandler(SessionBaseHandler):
    def initialize(self):

        self.access_token = None

    @coroutine
    def prepare(self):
        self.access_token = yield get_access_token()

        # 通过查询参数取出code后获取人员信息并进行缓存
        code = self.get_query_argument("code", None)
        if code :
            get_user_info_url = constant.QUERY_USER_INFO_URL % (self.access_token, code)
            response = yield send_request(get_user_info_url)
            result = json.loads(response.body)

            user_id = result.get('UserId', None)
            if user_id:
                self.session['user_id'] = user_id

        # 获取安全的code,并且缓存用户
        user_id = self.session.get('user_id', None)
        if not user_id:
            next_url = constant.BASE_URL + self.request.uri
            args = {"CorpID": self.settings[constant.WEIXIN_SETTINGS][constant.CorpID],
                    "redirect_uri": urlencode({'l':next_url})[2:]}
            url = constant.QUERY_AUTH_CODE_URL % args
            # response=yield  send_request(url)
            self.redirect(url)

        SessionBaseHandler.prepare(self)  # 调用父类方法
    @coroutine
    def get_current_user(self):
        """获取当前登陆的用户"""
        session_id=self.session.id
        if session_id:
            user_id=self.session.get('user_id',None)
            if not user_id:
                raise Return(None)
            else:
                url=constant.QUYER_USER_DEATIL_URL%(self.access_token,user_id)
                res = yield  send_request(url)

                raise Return(json.loads(res.body))


class IndexHandler(BaseHandler):

    @coroutine
    def get(self, *args, **kwargs):
        user_id=self.get_secure_cookie('userid')
        if user_id:
            self.write('userid')
        else:

            self.write(json.dumps(self.get_current_user()))
            #get
            pass

    @coroutine
    def post(self, *args, **kwargs):
        pass

class TestHanlder(RequestHandler):

    def get(self, *args, **kwargs):
        a="""<a href="https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx14c57c94c45b9c09&redirect_uri=http%3A%2F%2Ftest.chinasws.com%2Fmobile%2Findex.html&response_type=code&scope=snsapi_base&state=STATE#wechat_redirect">LinkME</a>"""
        self.write(a)


route = [(r'/mobile/index.html', IndexHandler),
         (r'/mobile/test.html',TestHanlder),]


if __name__== "__main__":
    pass