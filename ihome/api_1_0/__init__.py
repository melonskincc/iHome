# --*-- coding:utf-8 --*--
from flask.blueprints import Blueprint

#需求url:127.0.0.1:5000/api/1.0/index
api=Blueprint('api_1_0',__name__,url_prefix='/api/1.0')
#为了能调用到视图需要导入
from . import verify,passport,profile,house,order