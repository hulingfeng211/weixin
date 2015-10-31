# -*- coding:utf-8 -*-
"""
Describe:负责对微信App发送消息的相关请求的处理
"""
import json
import logging
import mimetypes
import urllib
import time
import xml.etree.cElementTree as ET

import requests
from tornado.gen import coroutine
from tornado.httpclient import AsyncHTTPClient
from tornado.ioloop import IOLoop
from tornado.web import HTTPError

import constant
from wechat import WeiXinRequstHandler, allow_media_file_types, generate_message, get_menu, callback
from wechat.WXBizMsgCrypt import WXBizMsgCrypt

__author__ = 'george'


class MessageHandler(WeiXinRequstHandler):
    """RESTFul服务接口，用于发送微信消息"""

    @coroutine
    def get(self, *args, **kwargs):
        self.write(self.access_token)

    @coroutine
    def post(self, *args, **kwargs):
        """接收外部调用给微信企业号发送消息
        对于请求的格式是一个json格式的字符串，格式如下:

        {"type":"text",
        "user":"someone",
        "content":{"content":"content"}
        "safe":"0"
        }
        content的内容跟type有关，可以参见微信的发送消息的说明:http://qydev.weixin.qq.com/wiki/index.php?title=%E6%B6%88%E6%81%AF%E7%B1%BB%E5%9E%8B%E5%8F%8A%E6%95%B0%E6%8D%AE%E6%A0%BC%E5%BC%8F
        如下：
        1.if type是text，content是{"content": "Holiday Request For Pony(http://xxxxx)"}
        2.if type是image，content是{"media_id": "MEDIA_ID"}  media_id可以从媒体接口中获取
        3.if type是voice，content是{"media_id": "MEDIA_ID"}  media_id可以从媒体接口中获取
        4.if type是video，content是{"media_id": "MEDIA_ID","title":"title","description":"description"}  media_id可以从媒体接口中获取
        5.if type是file，content是{"media_id": "MEDIA_ID"}  media_id可以从媒体接口中获取
        6.if type是news，content是{
                                   "articles":[
                                       {
                                           "title": "Title",
                                           "description": "Description",
                                           "url": "URL",
                                           "picurl": "PIC_URL"
                                       },
                                       {
                                           "title": "Title",
                                           "description": "Description",
                                           "url": "URL",
                                           "picurl": "PIC_URL"
                                       }
                                            ]
                                    }
        7.if type是mpnews,content是 {
                                       "articles":[
                                           {
                                               "title": "Title",
                                               "thumb_media_id": "id",
                                               "author": "Author",
                                               "content_source_url": "URL",
                                               "content": "Content",
                                               "digest": "Digest description",
                                               "show_cover_pic": "0"
                                           },
                                           {
                                               "title": "Title",
                                               "thumb_media_id": "id",
                                               "author": "Author",
                                               "content_source_url": "URL",
                                               "content": "Content",
                                               "digest": "Digest description",
                                               "show_cover_pic": "0"
                                           }
                                       ]
                                   },
                                   "safe":"0"
                                }

        :raise 服务只针对applicationjson的请求进行响应，非application/json的请求将返回500错误"""

        if "application/json" in self.request.headers['content-type']:
            content = json.loads(self.request.body)
        else:
            raise HTTPError(500, log_message="content-type 只支持application/json")

        if not content.get('content', None):
            raise HTTPError(500, log_message="发送内容为必填项")

        body = generate_message(content.get('type', 'text'),
                                content.get('user', ''),
                                content['content'],
                                self.settings[constant.WEIXIN_SETTINGS][constant.AgentId],
                                content.get('safe', 0))
        logging.info(body)
        send_message_url = constant.SEND_MESSAGE_URL % (self.access_token)
        response = yield AsyncHTTPClient().fetch(send_message_url, method="POST", body=body,
                                                 **self.settings[constant.PROXY_SETTINGS])
        if response:
            self.write(response.body)


class MenuHandler(WeiXinRequstHandler):
    @coroutine
    def get(self, *args, **kwargs):
        create_menu_url = constant.CREATE_MENU_URL % (
        self.access_token, self.settings[constant.WEIXIN_SETTINGS][constant.AgentId])
        body = json.dumps(get_menu(), ensure_ascii=False).encode('utf-8')
        response = yield AsyncHTTPClient().fetch(create_menu_url, method="POST", body=body,
                                                 **self.settings[constant.PROXY_SETTINGS])
        if response:
            self.write(response.body)


class CallbackHandler(WeiXinRequstHandler):
    @coroutine
    def get(self, *args, **kwargs):
        """验证回调URL的合法性"""
        weixin_settings = self.settings[constant.WEIXIN_SETTINGS]
        wxcpt = WXBizMsgCrypt(weixin_settings[constant.Token],
                              weixin_settings[constant.EncodingAESKey],
                              weixin_settings[constant.CorpID])
        msg_signature = self.get_argument('msg_signature', '')
        timestamp = self.get_argument('timestamp', '')
        nonce = self.get_argument('nonce', '')
        echostr = self.get_argument('echostr', '')
        ret, sEchoStr = wxcpt.VerifyURL(msg_signature, timestamp, nonce, echostr)
        if ret:
            self.write("Error:VerifyURL ret:%s" % ret)
            raise HTTPError(500, log_message="验证URL失败")
        else:
            self.write(sEchoStr)

    @coroutine
    def post(self, *args, **kwargs):
        """用于微信的回调模式的调用,不能超过5s响应请求，微信服务器会在5s后重试，重试3次。
        如果任务处理的时间超过5s可以先响应用户事件（直接响应200），处理完成后通过发送消息接口异步发送消息通知用户"""
        weixin_settings = self.settings[constant.WEIXIN_SETTINGS]
        wxcpt = WXBizMsgCrypt(weixin_settings[constant.Token],
                              weixin_settings[constant.EncodingAESKey],
                              weixin_settings[constant.CorpID])

        msg_signature = self.get_query_argument('msg_signature', '')
        timestamp = self.get_query_argument('timestamp', '')
        nonce = self.get_query_argument('nonce', '')

        data = self.request.body
        ret, msg = wxcpt.DecryptMsg(data, msg_signature, timestamp, nonce)
        if ret:
            logging.info('Error: DecryptMsg ret:' + str(ret))
            raise HTTPError(500, log_message="解密消息出错误")
        # 对明文进行处理,针对消息内容进行处理
        logging.info(msg)
        logging.info('begin extract')
        # ret,content,to_user=XMLParse.extract(msg)
        xml_tree = ET.fromstring(msg)
        msgtype = xml_tree.find('MsgType').text

        func = callback.message_type_handle_map.get(msgtype, None)
        if not func:  # 没有找到指定的处理方法
            self.write("")
            self.finish()
        if msgtype == 'event':
            event_type = xml_tree.find("Event").text
            IOLoop.current().add_timeout(time.time() + 1, func, event_type, xml_tree)
            # yield Task(func,event_type,xml_tree)
            # yield func(event_type,xml_tree)#处理各种事件消息
        else:
            IOLoop.current().add_timeout(time.time() + 1, func, xml_tree, wxcpt)
            # yield Task(func,xml_tree,wxcpt)
            # yield  func(xml_tree,wxcpt)#处理普通的消息


        # hulingfeng211@163.com
        response_template = """<xml><ToUserName><![CDATA[%(to_user)s]]></ToUserName>
        <FromUserName><![CDATA[%(from_user)s]]></FromUserName>
        <CreateTime>1348831860</CreateTime>
        <MsgType><![CDATA[text]]></MsgType>
        <Content><![CDATA[%(content)s]]></Content>
        <MsgId>1234567890123456</MsgId> <AgentID>128</AgentID></xml>"""
        response_content = {
            'to_user': xml_tree.find('FromUserName').text,
            'from_user': weixin_settings[constant.CorpID],
            'content': '您的请求已经被受理，稍后给你回复'
        }
        response_msg = response_template % response_content
        # auto replay
        ret, en_msg = wxcpt.EncryptMsg(response_msg, nonce, timestamp)
        self.write(en_msg)


class MediaHanlder(WeiXinRequstHandler):
    """负责上传所有的微信媒体附件"""

    @coroutine
    def get(self, *args, **kwargs):
        """获取所有的媒体资源列表"""
        body = {
            "type": args[0] if len(args) > 0 else 'file',
            "agentid": self.settings[constant.WEIXIN_SETTINGS][constant.AgentId],
            "offset": 0,
            "count": 50
        }
        url = constant.QUERY_MEDIA_URL % self.access_token
        response = yield AsyncHTTPClient().fetch(url, method="POST",
                                                 body=json.dumps(body, ensure_ascii=False).encode('utf-8'),
                                                 **self.settings[constant.PROXY_SETTINGS])
        if response:
            self.write(response.body)

    @coroutine
    def post(self, *args, **kwargs):
        file_meta = self.request.files.get('media', None)
        if file_meta:
            file_name = file_meta[0]['filename']
            file_type = mimetypes.guess_type(file_name)[0] or "other"
            type = allow_media_file_types.get(file_type, "file")

            upload_type = args[0] if len(args) > 0 else 'provisional'
            if upload_type == 'provisional':
                # 临时素材
                upload_file_url = constant.UPLOAD_PROVISIONAL_MEDIA_URL % (type, self.access_token)
            else:
                # 永久素材
                upload_file_url = constant.UPLOAD_FOREVER_MEDIA_URL % (
                self.settings[constant.WEIXIN_SETTINGS][constant.AgentId], type, self.access_token)

            proxy_host = self.settings[constant.PROXY_SETTINGS][constant.PROXY_HOST]
            proxy_port = self.settings[constant.PROXY_SETTINGS][constant.PROXY_PORT]
            proxies = None
            if proxy_host and proxy_port:
                proxies = {
                    "http": "http://%s:%s" % (proxy_host, proxy_port),
                    "https": "http://%s:%s" % (proxy_host, proxy_port),
                }
            if file_type is None:
                raise HTTPError(status_code=500, log_message="需要明确指定文件的后缀名")

            filename = urllib.urlencode({"a": file_name})[2:]
            files = {'file': (filename, file_meta[0]['body'])}
            response = requests.post(upload_file_url, files=files, proxies=proxies)
            if response:
                logging.info(response.text)
                self.write(json.loads(response.text))
            else:
                logging.info("error")


route = [
    (r'/weixin/message/send', MessageHandler),
    (r'/weixin/message/callback', CallbackHandler),
    (r'/weixin/media', MediaHanlder),
    (r'/weixin/media/(.*)', MediaHanlder),
    (r'/weixin/menu', MenuHandler),
    (r'/weixin/media/(.*)', MediaHanlder),
]
