# --*-- coding:utf-8 --*--
from flask.blueprints import Blueprint
from flask import current_app, make_response
from flask_wtf import csrf

static_html=Blueprint('static_html',__name__)
@static_html.route('/<re(".*"):file_name>')
def get_static_html(file_name):
    """
    需求：
    1.前端请求返回静态页面
    2.输入127.0.0.1:5000/  或者 127.0.0.1:5000/index.html  显示首页
    3.浏览器自动请求favicon.ico
    """
    # 输入为空
    if not file_name:
        file_name='index.html'
    # 不是网页头像请求
    if file_name!='favicon.ico':
        file_name='html/'+file_name

    # 因为post请求需要CSRF认证所以在每次响cookie中加入CSRF_TOKEN
    response=make_response(current_app.send_static_file(file_name))
    csrf_token=csrf.generate_csrf()
    response.set_cookie('csrf_token',csrf_token)
    return response