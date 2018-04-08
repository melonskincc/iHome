# --*-- coding:utf-8 --*--
import qiniu

#七牛access_key
from flask import current_app

access_key = "yV4GmNBLOgQK-1Sn3o4jktGLFdFSrlywR2C-hvsW"
#七牛secret_key
secret_key = "bixMURPL6tHjrb8QKVg2tm7n9k8C7vaOeQ4MEoeW"
#上传的空间名
bucket_name = 'ihome'

def upload_image(data):
    """上传图片方法"""
    # 构建鉴权对象
    q=qiniu.Auth(access_key,secret_key)
    # 生成上传token,可以指定过期时间
    token=q.upload_token(bucket_name)
    #设置文件名
    # key=data.filename
    # 上传二进制文件流
    ret,info=qiniu.put_data(token,None,data)
    #返回结果：({u'hash': u'FrsdIVZsIZA6p4WXOzdxBLxiyQ2O', u'key': u'avatar'},
    # exception:None, status_code:200)
    if 200==info.status_code:
        return ret.get('key')
    else:
        raise Exception('上传图片到七牛云失败')

