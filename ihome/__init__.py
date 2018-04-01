# --*-- coding:utf-8 --*--
from flask import Flask
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from config import configs
from ihome.utils.my_converters import RegexConverter

#启动项目就创建app
db=SQLAlchemy()

def get_app(config_name):
    """
    app工厂函数
    :param config_name: 传入现在开发的环境名字
    :return: 返回app
    """
    # 创建app
    app = Flask(__name__)
    # 加载配置文件
    app.config.from_object(configs[config_name])
    # 创建数据库连接对象,赋值给全局db
    global db
    db = SQLAlchemy(app)
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
