# --*-- coding:utf-8 --*--
from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_migrate import Migrate,MigrateCommand
from flask_script import Manager
from flask_session import Session
from flask_wtf.csrf import CSRFProtect

#创建app
app=Flask(__name__)
#加载配置文件
app.config.from_object(Config)
#创建数据库连接对象
db=SQLAlchemy(app)
#让迁移时，app和数据库建立关联
Migrate(app,db)
#创建脚本管理器
manager=Manager(app)
#增加db脚本命令
manager.add_command('db',MigrateCommand)
#session绑定app
Session(app)
#开启CSRF保护
CSRFProtect(app)

#测试视图
@app.route('/',methods=['GET','POST'])
def index():
    # redis数据库存储session测试
    session['name']='hahaha'
    return 'index'

if __name__ == '__main__':
    app.run()