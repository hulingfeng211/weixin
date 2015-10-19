# -*- coding:utf-8 -*-
from datetime import datetime
import time
import logging
from tornado.gen import coroutine, Task
from tornado.httpclient import HTTPRequest, AsyncHTTPClient
from tornado.ioloop import IOLoop
import config
import constant
from core import redis, db, redis_send

@coroutine
def subscribe():
    yield Task(redis.subscribe,'send_message')
    redis.listen(callback=on_recieve_message)

@coroutine
def on_recieve_message(content):

    logging.info('on_recieve_message running...')
    if content.kind=='message':
        headers={
            'content-type':"application/json"
        }
        """
        conent.body: { mobile:item[0],
                    content:item[1],
                    time:item[2],
                    extno:item[3] }
        extno:扩展码＋自定义的扩展码
                    """
        try:
            logging.info(content.body)
            request=HTTPRequest(config.PUSH_URL,'POST',headers=headers,body=content.body.encode('utf-8'))
            logging.info(config.PUSH_URL)
            response=yield AsyncHTTPClient().fetch(request)
        except Exception,reason:
            yield db.smslog.insert(dict(
                message=reason.message,
                args=content.body
            ))
@coroutine
def loop_send_message():
    """循环发送队列中的消息"""
    redis_send.rpoplpush(constant.SOURCE_MESSAGE_CHANNEL,constant.DEST_MESSAGE_CHANNEL,callback=on_send_message)

@coroutine
def on_send_message(args):
    if args is not None:
        logging.info(args)
        header = {
            "content-type": "application/x-www-form-urlencoded"
        }
        request=HTTPRequest(config.SERVICE_URL,method="POST",headers=header,body=args,**config.PROXY_SETTINGS)
        try:
            response= yield AsyncHTTPClient().fetch(request)

            if response :
                 #保存发送记录
                 if response.body and response.body[0]=="0":#提交成功
                     logging.info(response.body)
                     response_array=response.body.split(',')
                     if len(response_array)>5:

                         yield db.sendrecord.insert(dict(
                         code=response_array[0],
                         sendid=response_array[1],
                         invalidcount=response_array[2],
                         successcount=response_array[3],
                         blackcount=response_array[4],
                         msg=response_array[5],
                         message=args
                     ))
                 else:
                     yield db.smslog.insert(dict(
                         time=datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S'),
                     message=response.body,
                     ))
            redis_send.lrem(constant.DEST_MESSAGE_CHANNEL,args)
            #todo 状态报告回调
        except Exception,e:
            redis_send.rpoplpush(constant.DEST_MESSAGE_CHANNEL,constant.SOURCE_MESSAGE_CHANNEL)
            logging.info(e)

    IOLoop.current().add_timeout(time.time()+10,loop_send_message)
