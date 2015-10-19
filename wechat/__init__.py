# -*- coding:utf-8 -*-
import json
import logging
import os

from tornado import gen
from tornado.gen import coroutine, Task
from tornado.httpclient import AsyncHTTPClient
from tornado.ioloop import IOLoop
from tornado.web import RequestHandler
from core import settings

import constant

__author__ = 'george'


@coroutine
def get_access_token():
    """获取微信的access_token"""
    access_token = yield Task(settings['redis'].get, constant.ACCESS_TOKEN)
    if access_token:
        raise gen.Return(access_token)
    else:
        corpid = settings[constant.WEIXIN_SETTINGS].get(constant.CorpID)
        corpsecret = settings[constant.WEIXIN_SETTINGS].get(constant.Secret)
        access_token_url = constant.ACCESS_TOKEN_URL % (corpid, corpsecret)
        try:
            response = yield AsyncHTTPClient().fetch(access_token_url, **settings[constant.PROXY_SETTINGS])
            if response and response.code == 200:
                logging.info(response.body)
                access_token_json = json.loads(response.body)
                access_token = access_token_json.get('access_token')

                # cache access_token to redis
                yield Task(settings['redis'].set, constant.ACCESS_TOKEN, access_token,
                           expire=access_token_json.get('expires_in'))
                raise gen.Return(access_token)
        except Exception, e:
            raise gen.Return(access_token)

def generate_media_message(users,content,agentid,type,safe=0):
    """生成图片、声音、文件三类消息"""
    body = {
        "touser": users if isinstance(users,unicode) or isinstance(users,str) else reduce(lambda x,y:x+'|'+y,users),
        "toparty": "",
        "totag": "",
        "msgtype": type,
        "agentid": agentid,
        type:content,
        "safe": safe
    }
    return type,body

#@coroutine
def get_menu():
    """创建微信菜单"""
    path=os.path.join(os.path.dirname(__file__),"menu.json")
    with open(path,'rb') as f:
        menu_str= reduce(lambda x,y:x+y,f.readlines())
        return json.loads(menu_str)


def generate_message(type,users,content,agentid,safe=0):
    """生成要发送的消息"""
    func=message_type_tuple.get(type,generate_message)
    type,body=func(users,content,agentid,type,safe)
    return json.dumps(body,ensure_ascii=False).encode('utf-8')


message_type_tuple={
    'text':generate_media_message,
    'image':generate_media_message,
    'voice':generate_media_message,
    'file':generate_media_message,
    'video':generate_media_message,
    'news':generate_media_message,
    'mpnews':generate_media_message,
}

class WeiXinRequstHandler(RequestHandler):
    @coroutine
    def prepare(self):
        access_token = yield get_access_token()
        self.access_token = access_token


allow_media_file_types={
    'video/mp4':"video",
    "image/png":"image",
    "image/jpg":"image",
    "audio/AMR":"voice",
    "other":"file"
}
if __name__=="__main__":
    #IOLoop.current().run_sync(get_menu)
    print get_menu()


