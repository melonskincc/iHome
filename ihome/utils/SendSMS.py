#coding=gbk

#coding=utf-8

#-*- coding: UTF-8 -*-  

from ihome.libs.yuntongxun.CCPRestSDK import REST
import ConfigParser

#主帐号
accountSid= '8a216da8627648690162843e217602d5'

#主帐号Token
accountToken= ''

#应用Id
appId='8a216da8627648690162843e21d002db'

#请求地址，格式如下，不需要写http://
serverIP='app.cloopen.com'

#请求端口 
serverPort='8883'

#REST版本号
softVersion='2013-12-26'

class CCP(object):
    """自定义单例类，用于发短信"""
    #用于记录实例
    __instance=None
    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            #没被实例化，记录第一次实例对象
            cls.__instance=super(CCP, cls).__new__(cls,*args, **kwargs)

            # 初始化REST SDK
            cls.__instance.rest = REST(serverIP, serverPort, softVersion)
            cls.__instance.rest.setAccount(accountSid, accountToken)
            cls.__instance.rest.setAppId(appId)
        return cls.__instance

    def send_sms(self,to, datas, tempId):
        """发送消息接口"""
        # 调用发送消息接口返回的：发送消息的结果
        result = self.rest.sendTemplateSMS(to, datas, tempId)
        if result.get('statusCode') == '000000':   # 发送成功返回的状态码
            return 1
        else:
            return 0

  # 发送模板短信
  # @param to 手机号码
  # @param datas 内容数据 格式为数组 例如：{'12','34'}，如不需替换请填 ''
  # @param $tempId 模板Id

# def sendTemplateSMS(to,datas,tempId):
#
#     #初始化REST SDK
#     rest = REST(serverIP,serverPort,softVersion)
#     rest.setAccount(accountSid,accountToken)
#     rest.setAppId(appId)
#
#     result = rest.sendTemplateSMS(to,datas,tempId)
#     for k,v in result.iteritems():
#
#         if k=='templateSMS' :
#                 for k,s in v.iteritems():
#                     print '%s:%s' % (k, s)
#         else:
#             print '%s:%s' % (k, v)
#
   
#sendTemplateSMS(手机号码,内容数据,模板Id)
