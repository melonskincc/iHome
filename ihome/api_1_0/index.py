# --*-- coding:utf-8 --*--
from flask import session
from . import api

# 测试视图
@api.route('/',methods=['GET','POST'])
def index():
    # redis数据库存储session测试
    session['name']='hahaha'
    return 'index'