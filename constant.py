# -*- coding:utf-8 -*-
__author__ = 'george'

#微信相关设置
ACCESS_TOKEN_URL="https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=%s&corpsecret=%s"
SEND_MESSAGE_URL='https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=%s'
UPLOAD_PROVISIONAL_MEDIA_URL='https://qyapi.weixin.qq.com/cgi-bin/media/upload?type=%s&access_token=%s'
#永久素材上传
UPLOAD_FOREVER_MEDIA_URL='https://qyapi.weixin.qq.com/cgi-bin/material/add_material?agentid=%s&type=%s&access_token=%s'
QUERY_MEDIA_URL='https://qyapi.weixin.qq.com/cgi-bin/material/batchget?access_token=%s'
CREATE_MENU_URL='https://qyapi.weixin.qq.com/cgi-bin/menu/create?access_token=%s&agentid=%s'

ACCESS_TOKEN="access_token"
WEIXIN_SETTINGS="weixin_settings"
CorpID='CorpID'
Secret='Secret'
AgentId='AgentId'
Token='Token'
EncodingAESKey='EncodingAESKey'

#END 微信

#代理
PROXY_SETTINGS="proxy_settings"