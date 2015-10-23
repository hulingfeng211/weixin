# -*- coding:utf-8 -*-
"""
Description:
"""
import logging
import os

from tornado.gen import coroutine, Return
from tornado.httpclient import AsyncHTTPClient

import constant
from core import settings
from core.utils import send_request
from wechat import get_access_token, generate_message

__author__ = 'george'

@coroutine
def deal_with_text_message(message,*args,**kwargs):
    """处理普通的文本消息"""
    logging.info(message)
    body={
        "tousername":message.find('ToUserName').text,
        "fromusername":message.find('FromUserName').text,
        "createtime":message.find('CreateTime').text,
        "msgtype":message.find('MsgType').text,
        "content":message.find('Content').text,
        "msgid":message.find('MsgId').text,
        "agentid":message.find('AgentID').text

    }
    #todo 自动回复内容到发送消息的用户
    #time.sleep(10)  #block 10s
    # sleep(10) #noblock 10s
    # 当用户输入消息字符长度为11位时，默认认为时托盘号，返回托盘明细的图文消息
    if len(body['content'])==8: # 新浪股票
        url=constant.SINA_STOCK_URL%body['content']
        res=yield send_request(url)
        result=res.body.strip()[:-1].split('=')[1][1:-1].split(',')
        if len(result)>1: # 正确取到数据
            message_body = {
            "articles": [
                {
                    "title": "股票代码:[%s] 股票:[%s]" % (body['content'],result[0].decode('gb2312').encode('utf-8')),
                    "thumb_media_id": "2NDpAUrBpMTQjFYMqFv_CqeEyxDx1jkYWABfC2-L08MLNzp6KdfzNvcGJHApkx7trKaapH8VEQ2KjAS2Uo0q7Bw",
                    "author": "新浪财经",
                    "content": "%s"%result,
                    "digest": "当前成交价:%s"%result[3],
                }]
        }

            yield send_message(message.find('FromUserName').text, message_body,
                           settings[constant.WEIXIN_SETTINGS][constant.AgentId], 'mpnews')

        else :
            message_body = {"content": "请确认你输入的股票代码【" + body['content'] + '】是否正确或存在?'}
            yield send_message(body['fromusername'], message_body, settings[constant.WEIXIN_SETTINGS][constant.AgentId],"text")

    elif len(body['content']) == 11:
        message_body = {
            "articles": [
                {
                    "title": "[%s]明细" % body['content'],
                    "thumb_media_id": "2NDpAUrBpMTQjFYMqFv_CqeEyxDx1jkYWABfC2-L08MLNzp6KdfzNvcGJHApkx7trKaapH8VEQ2KjAS2Uo0q7Bw",
                    "author": "胡佐治测试",
                    "content": "t",
                    "digest": "点击查看托盘明细",
                }]
        }
        content = ''
        file_path = os.path.join(os.path.dirname(__file__), '224FP120151.txt')
        all_lines = [line for line in open(file_path)]
        for item in all_lines:
            tmp=item.split(',')
            content+='<div>'
            content+='<h2>编号:%s</h2>'%tmp[0]
            content+='<h2>描述:%s</h2>'%tmp[1]
            content+='<h2>数量:%s</h2>'%tmp[2]
            content+='<h2>其他:%s</h2>'%tmp[3]
            content+='</div>'
            content+='<hr/>'

        message_body['articles'][0]['content'] = content
        yield send_message(message.find('FromUserName').text, message_body,
                           settings[constant.WEIXIN_SETTINGS][constant.AgentId], 'mpnews')

    else:
        message_body = {
            "content": "来自服务器的消息,针对【" + body['content'] + '】的回复'
        }
        yield send_message(body['fromusername'], message_body, settings[constant.WEIXIN_SETTINGS][constant.AgentId],
                           'text')
    if 'callback' in kwargs:
        callback=kwargs.pop('callback')
        callback(body,*args,**kwargs)
    raise Return(body)

@coroutine
def deal_with_image_message(message,*args,**kwargs):
    """处理普通的image消息"""
    logging.info(message)
    pass

@coroutine
def deal_with_voice_message(message,*args,**kwargs):
    """处理录音消息"""
    logging.info(message)
    pass

@coroutine
def deal_with_video_message(message,*args,**kwargs):
    """处理视频"""
    logging.info(message)
    pass

@coroutine
def deal_with_shortvideo_message(message,*args,**kwargs):
    """处理短视频消息"""
    logging.info(message)
    pass

@coroutine
def deal_with_location_message(message,*args,**kwargs):
    """处理location消息"""
    logging.info(message)
    pass


@coroutine
def deal_with_event_message(type,message,*args,**kwargs):
    """处理各种事件"""
    logging.info(type)
    logging.info(event_type_handle_map)
    func = event_type_handle_map.get(type)
    if func:
        yield func(type, message, *args, **kwargs)


@coroutine
def deal_with_install_tray_click(type, message, *args, **kwargs):
    """"""
    # 返回安装托盘列表给当前点击菜单的用户,发送图文消息
    message_body = {
        "articles": [
            {
                "title": "安装托盘列表",
                "thumb_media_id": "2NDpAUrBpMTQjFYMqFv_CqeEyxDx1jkYWABfC2-L08MLNzp6KdfzNvcGJHApkx7trKaapH8VEQ2KjAS2Uo0q7Bw",
                "author": "胡佐治测试",
                "content": "t",
                "digest": "点击查看与你相关的托盘",
            }]
    }
    body = {
        "tousername": message.find('ToUserName').text,
        "fromusername": message.find('FromUserName').text,
        "createtime": message.find('CreateTime').text,
        "msgtype": message.find('MsgType').text,
        "event": message.find('Event').text,
        "eventkey": message.find('EventKey').text,
        "agentid": message.find('AgentID').text

    }
    table_header = ["托盘号", "托盘描述", "总数量"]
    file_path = os.path.join(os.path.dirname(__file__), '2015-38.txt')
    all_lines = [line for line in open(file_path)]
    data_dict = []
    for line in all_lines:
        tmp = line.split(',')
        data_dict.append({
            'shipno': tmp[1],
            'trayno': tmp[2],
            'traydesc': tmp[3],
            'orgn': tmp[4],
            'total': tmp[5],
            'weekno': tmp[6],
        })
    group_tray_list = {}
    for item in data_dict:
        ship_no = item.get('shipno')
        if group_tray_list.has_key(ship_no):
            group_tray_list[ship_no].append(item)
        else:
            group_tray_list[ship_no] = []
            group_tray_list[ship_no].append(item)

    content = ''
    for key, val in group_tray_list.items():
        content += '<h2>船号：%s</h2>' % key
        content += '<h2>周编号：%s</h2>' % group_tray_list[key][0]['weekno']
        content += '<h2>部门：%s</h2>' % group_tray_list[key][0]['orgn']
        content += '<table >'
        # header
        content += '<tr>'
        for item in table_header:
            content += '<th>' + item + '</th>'
        content += '</tr>'
        # end header
        # body
        for value in val:
            content += '<tr>'
            content += '<td>' + str(value.get('trayno')) + '</td>'
            content += '<td>' + str(value.get('traydesc')) + '</td>'
            content += '<td>' + str(value.get('total')) + '</td>'
            content += '</tr>'
        content += "</table>"
        content += '<hr/>'

    message_body['articles'][0]['content'] = content
    yield send_message(message.find('FromUserName').text, message_body,
                       settings[constant.WEIXIN_SETTINGS][constant.AgentId], 'mpnews')
    if 'callback' in kwargs:
        callback = kwargs.pop('callback')
        callback(body, *args, **kwargs)
    raise Return(body)


@coroutine
def deal_with_click_event(type, message, *args, **kwargs):
    """处理Click事件"""
    func = click_event_handle_map.get(message.find('EventKey').text)
    yield func(type, message, *args, **kwargs)


@coroutine
def send_message(users,content,agentid,type):
    """发送消息到指定的用户"""
    access_token=yield get_access_token()
    body=generate_message(type,users,content,agentid)
    logging.info(body)
    send_message_url=constant.SEND_MESSAGE_URL%(access_token)
    response=yield AsyncHTTPClient().fetch(send_message_url,method="POST",body=body,**settings[constant.PROXY_SETTINGS])
    if response:
        logging.info(response.body)

message_type_handle_map={
    "text":deal_with_text_message,#text消息
    "image":deal_with_image_message,#image消息
    "voice":deal_with_voice_message,#voice消息
    "video":deal_with_video_message,#video消息
    "shortvideo":deal_with_shortvideo_message,#小视频消息
    "location":deal_with_location_message,#location消息
    "event":deal_with_event_message#事件的消息
}
click_event_handle_map = {
    "key_2_2": deal_with_install_tray_click  #
}

event_type_handle_map={

    # **********事件***************
    'subscribe':"",  #当用户关注微信号的事件
    'unsubscribe':"",  #当用户取消关注的事件
    'location': "",  # 当用户上报地理位置的事件
    'click': deal_with_click_event,  # 点击菜单拉取消息的事件
    'view': "",  #点击菜单跳转链接的事件
    'scancode_push':"",  #当用户点击菜单触发扫描二维码的事件
    'scancode_waitmsg':"",  #扫码推事件且弹出“消息接收中”提示框的事件推送
    'pic_sysphoto':"",  #弹出系统拍照发图的事件推送
    'pic_photo_or_album':"",  #弹出拍照或者相册发图的事件推送
    'pic_weixin':"",  #弹出微信相册发图器的事件推送
    'location_select':"",  #弹出地理位置选择器的事件推送
    'enter_agent':"",  #成员进入应用的事件推送
    'batch_job_result':"",#异步任务完成事件推送
}

