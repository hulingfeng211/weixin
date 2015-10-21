# -*- coding:utf-8 -*-
import hashlib

from bson.objectid import ObjectId
import motor
from tornado.httpclient import HTTPRequest, AsyncHTTPClient
from tornado.gen import  Return
import tornadoredis
import constant

__author__ = 'george'
import config
import json
from json import JSONEncoder
from pymongo import MongoClient
from tornado.gen import coroutine

# init mongodb and redis client
db = motor.MotorClient(config.MONGO_URL).smscenter
dbsync = MongoClient(config.MONGO_URL).smscenter
redis = tornadoredis.Client(host=config.REDIS_SETTINGS['host'],selected_db=config.REDIS_SETTINGS['db'])
# redis_send = tornadoredis.Client(host=config.REDIS_SETTINGS['host'],selected_db=config.REDIS_SETTINGS['db'])
redis_reciver = tornadoredis.Client(host=config.REDIS_SETTINGS['host'],selected_db=config.REDIS_SETTINGS['db'])

redis_reciver.connect()
# redis_send.connect()
redis.connect()


def load_setting():
    """加载配置文件"""
    object_list = dir(config)
    setting = {}
    for item in object_list:
        if item.isupper():
            setting[item.lower()] = getattr(config, item)
    setting['db'] = db
    setting['dbsync'] = dbsync
    setting['redis'] = redis
    setting['redis_reciver'] = redis_reciver
    return setting


def generate_response(status='success', status_code=200, message='Success'):
    """生成返回消息"""
    return  json.dumps(dict({
        'status':status,
        'status_code':status_code,
        'message':message
    }))


def is_json_request(request):
    """判断tornado的请求是否是application/json请求
    :param request tornado的web模块的request对象
    :return 返回True or False"""
    return 'application/json' in request.headers['Content-Type']


def clone_dict_without_id(obj):
    """复制一个字典对象，去除字典的id列
    :param obj 字典类型的对象
    :return 返回新生成的字典类型"""
    #return {key: val for key, val in obj.items() if key != "_id" and key != "id"}
    newobj={}
    for key, val in obj.items():
        if key == '_id' or key == "id":
            continue
        newobj[key]=val


class MongoEncoder(JSONEncoder):
    """针对mongodb中ObjectId进行序列化的封装"""
    def default(self, o,**kwargs):
        if isinstance(o,ObjectId):
            return str(o)
        else:
            return JSONEncoder.default(o,**kwargs)


def bson_encode(obj):
    """针对mongodb中的文档进行json格式序列化方法的封装
    :param obj 需要进行序列化的对象可以是mongodb的文档或dict类型
    :return 返回序列化后的json字符串"""
    return json.dumps(obj,cls=MongoEncoder)






settings = load_setting()


if __name__ == "__main__":
    print load_setting()
