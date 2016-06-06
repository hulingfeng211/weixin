#!/usr/bin/env python
# -*- coding:utf-8 -*- 
"""========================================================== 
+FileName:config.py
+Author: george
+mail:hulingfeng211@163.com
+Created Time:2015年07月22日 星期三 10时48分55秒
+Description:应用程序配置文件
+============================================================"""
import os

# 开启程序的debug模式
DEBUG=True

# 指定静态文件的路经
STATIC_PATH=os.path.join(os.path.dirname(__file__),"static")

# 安全Cookie设置,生成请参见README.md
COOKIE_SECRET = "YaEw9bPmScGNisoXLNjvxUF7SbYBm0+tsV4WMyNZqXc=",

# 指定模版文件的路经
TEMPLATE_PATH=os.path.join(os.path.dirname(__file__),'templates')
# TEMPLATE_PATH=os.path.join(os.path.dirname(__file__),'front')

# 系统代理设置
PROXY_SETTINGS = {
    "proxy_host": "192.168.2.7",
    "proxy_port": 3128
}

REDIS_SETTINGS = {
    "host": "192.168.2.14",
    "port": 6379,
    "db": 15
}
# SESSION相关的配置
SESSION = {
    "driver": 'redis',
    "driver_settings": dict(
        host='192.168.2.7',
        port=6379,
        db=16,
        max_connections=1024
    )
}

MONGO_URL = "mongodb://192.168.2.14:27017"


# 微信设置
WEIXIN_SETTINGS = {
    "CorpID": "wx14c57c94c45b9c09",
    "Secret": "k3yqQQjyMWkwBrNNj5E-Dxwleyh-la2CEBTFzRe05sMFZnR7AhZN33F03CXApmOW",  # 测试管理员组的Secret
    "AgentId": 3,
    "Token": "qC7nq53RTJcCzsNwcnklXxymBwfUd99",
    "EncodingAESKey": "rp6jgUcEAuh70oz5nPwF2BKtJq7nd3OFdskPdjnmEdi"
}
# END微信设置