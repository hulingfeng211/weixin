# -*- coding:utf-8 -*-
"""==========================================================
|   FileName:mobile.py
|   Author: george
|   mail:hulingfeng211@163.com
|   Created Time:2015年10月19日 星期一 14时17分03秒
|   Description:项目中的所有系统常量
+============================================================"""
# 微信相关设置
ACCESS_TOKEN_URL="https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=%s&corpsecret=%s"
SEND_MESSAGE_URL='https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=%s'
UPLOAD_PROVISIONAL_MEDIA_URL='https://qyapi.weixin.qq.com/cgi-bin/media/upload?type=%s&access_token=%s'
QUERY_AUTH_CODE_URL = u"https://open.weixin.qq.com/connect/oauth2/authorize?appid=%(CorpID)s&redirect_uri=%(redirect_uri)s&response_type=code&scope=snsapi_base&state=STATE#wechat_redirect"
QUERY_USER_URL = 'https://qyapi.weixin.qq.com/cgi-bin/user/getuserinfo?access_token=%s&code=%s'
QUERY_USER_INFO_URL='https://qyapi.weixin.qq.com/cgi-bin/user/getuserinfo?access_token=%s&code=%s'
QUYER_USER_DEATIL_URL='https://qyapi.weixin.qq.com/cgi-bin/user/get?access_token=%s&userid=%s'

# 永久素材上传
UPLOAD_FOREVER_MEDIA_URL='https://qyapi.weixin.qq.com/cgi-bin/material/add_material?agentid=%s&type=%s&access_token=%s'

QUERY_MEDIA_URL='https://qyapi.weixin.qq.com/cgi-bin/material/batchget?access_token=%s'
CREATE_MENU_URL='https://qyapi.weixin.qq.com/cgi-bin/menu/create?access_token=%s&agentid=%s'

# 新浪财经股票数据
SINA_STOCK_URL = 'http://hq.sinajs.cn/list=%s' # 股票代码
BASE_URL = "http://test.chinasws.com"
ACCESS_TOKEN = "access_token"
WEIXIN_SETTINGS = "weixin_settings"
CorpID = 'CorpID'
Secret = 'Secret'
AgentId = 'AgentId'
Token = 'Token'

EncodingAESKey='EncodingAESKey'

# END 微信

# 代理
PROXY_SETTINGS = "proxy_settings"
PROXY_HOST='proxy_host'
PROXY_PORT='proxy_port'
