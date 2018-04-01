# --*-- coding:utf-8 --*--
from flask import session
from flask_migrate import Migrate,MigrateCommand
from flask_script import Manager
from ihome import get_app,db

app=get_app('develop')
#让迁移时，app和数据库建立关联
Migrate(app,db)
#创建脚本管理器
manager=Manager(app)
#增加db脚本命令
manager.add_command('db',MigrateCommand)

if __name__ == '__main__':
    print app.url_map
    manager.run()