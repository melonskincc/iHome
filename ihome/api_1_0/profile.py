# --*-- coding:utf-8 --*--
from flask import g, current_app, jsonify, session
from ihome.api_1_0 import api
from ihome.models import User
from ihome.utils.common import login_required
from ihome.utils.response_code import RET

@api.route('/users')
@login_required
def get_user_info():
    """获取用户信息:
    1.登录校验  @login_required
    2.g变量中获取user_id
    3.查询user
    :return: 返回响应，用户信息
    """
    user_id=g.user_id
    try:
        user=User.query.get(user_id)
    except Exception as e:
        current_app.logger.debug(e)
        return jsonify(re_code=RET.DBERR,msg='查询用户失败')
    if not user:
        return jsonify(re_code=RET.NODATA,msg='用户不存在')
    #查询出用户信息
    user_info=user.to_dict()
    return jsonify(re_code=RET.OK,msg='查询成功',user=user_info)

@api.route('/sessions')
def check_login():
    """用户判断用户是否登录的接口：方便前端工作
    1.获取session中的user_id,name
    :return: user_id,name
    """
    user_id=session.get('user_id')
    name=session.get('name')

    return jsonify(re_code=RET.OK,msg='OK',user={'user_id':user_id,'name':name})