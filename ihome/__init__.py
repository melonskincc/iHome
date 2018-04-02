# --*-- coding:utf-8 --*--
import logging
from logging.handlers import RotatingFileHandler

import redis
from flask import Flask
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from config import configs
from ihome.utils.my_converters import RegexConverter

#定义能被外部调用的对象
db=SQLAlchemy()
redis_conn=None

def setupLogging(levle):
    # 业务逻辑已开启就加载日志
    # 设置日志的记录等级
    logging.basicConfig(level=levle)  # 调试debug级
    # 创建日志记录器，指明日志保存的路径、每个日志文件的最大大小、保存的日志文件个数上限
    file_log_handler = RotatingFileHandler("logs/log", maxBytes=1024 * 1024 * 100, backupCount=10)
    # 为全局的日志工具对象（flask app使用的）添加日志记录器
    logging.getLogger().addHandler(file_log_handler)

def get_app(config_name):
    """
    app工厂函数
    :param config_name: 传入现在开发的环境名字
    :return: 返回app
    """
    # 调用封装的日志
    setupLogging(configs[config_name].LOGGIONG_LEVEL)

    # 创建app
    app = Flask(__name__)
    # 加载配置文件
    app.config.from_object(configs[config_name])

    # 创建数据库连接对象,赋值给全局db
    # global db
    # db=SQLAlchemy(app)
    db.init_app(app)

    # 创建Redis数据库连接对象
    global redis_conn
    redis_conn = redis.StrictRedis(host=configs[config_name].REDIS_HOST, port=configs[config_name].REDIS_PORT)

    # session绑定app
    Session(app)

    # 开启CSRF保护
    CSRFProtect(app)

    # 自定义转换器加入到默认转换器列表中
    app.url_map.converters['re']=RegexConverter

    #哪里需要哪里导入蓝图
    from ihome.api_1_0 import api
    from ihome.static_html import static_html
    #注册蓝图
    app.register_blueprint(api)
    app.register_blueprint(static_html)

    return app
