# -*- coding:utf-8 -*-
"""
功能描述:实用工具类包括 httputil
"""
import hashlib
from tornado.gen import coroutine, Return
from tornado.httpclient import HTTPRequest, AsyncHTTPClient
import constant
from core import settings

__author__ = 'george'


@coroutine
def send_request(url, method="GET", data=None, headers=None, **kwargs):
    """发送HTTP请求的封装
    :param url 目标资源
    :param method HTTP请求方法，默认GET
    :param data 需要发送的数据，如果是GET请求，默认忽略该参数
    :param headers 请求需要携带的HTTP头部信息

     :return 返回请求后的response对象 """
    # todo 待实现
    if not kwargs:
        kwargs = {}
        kwargs[constant.PROXY_HOST] = settings[constant.PROXY_SETTINGS][constant.PROXY_HOST]
        kwargs[constant.PROXY_PORT] = settings[constant.PROXY_SETTINGS][constant.PROXY_PORT]
    else:
        kwargs.update(settings[constant.PROXY_SETTINGS])

    request = HTTPRequest(url=url,method=method,body=data,headers=headers,**kwargs)
    response=yield AsyncHTTPClient().fetch(request)
    raise Return(response)


def make_password(password):
    """生成用户的加密后的密码，默认采用md5算法
    :param password 明文的密码
    :return md5加密后的密文密码"""
    return hashlib.md5(password).hexdigest()
