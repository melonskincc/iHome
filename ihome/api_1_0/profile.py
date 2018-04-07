# --*-- coding:utf-8 --*--
from flask import g, current_app, jsonify, session, request

from ihome import db, constants
from ihome.api_1_0 import api
from ihome.models import User
from ihome.utils.common import login_required
from ihome.utils.qiniu_image_storage import upload_image
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

@api.route('/users',methods=['PUT'])
@login_required
def update_user_name():
    """修改用户信息视图函数：
    0.登录校验  @login_required
    1.获取参数 name
    2.查询用户，更新用户名
    :return: 响应结果
    """
    json_dict=request.json
    user_id=g.user_id
    name=json_dict.get('name')
    if not name:
        return jsonify(re_code=RET.PARAMERR,msg='用户名不能为空')
    try:
        user=User.query.get(user_id)
    except Exception as e:
        current_app.logger.debug(e)
        return jsonify(re_code=RET.DBERR,msg='查询用户失败')
    if not user:
        return jsonify(re_code=RET.NODATA,msg='用户不存在')
    user.name=name
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.debug(e)
        return jsonify(re_code=RET.DBERR,msg='保存用户信息失败')
    return jsonify(re_code=RET.OK,msg='更新用户名成功')

@api.route('/users/avatar',methods=['POST'])
@login_required
def update_user_avatar():
    """修改用户头像：
    0.登录校验 @login_required
    :param  前端传来的image文件,g变量中的user_id
    1.上传到七牛云
    2.返回key，保存到数据库
    :return: 成功返回用户头像
    """
    # 获取图片数据
    avatar=request.files.get('avatar')
    user_id=g.user_id
    if not avatar:
        return jsonify(re_code=RET.PARAMERR,msg='图片不能为空')

    # 1.上传到七牛云
    key=upload_image(avatar)
    # 2.保存到数据库
    try:
        user=User.query.get(user_id)
    except Exception as e :
        current_app.logger.debug(e)
        return jsonify(re_code=RET.DBERR,msg='查询用户失败')
    if not user:
        return jsonify(re_code=RET.NODATA,msg='用户不存在')
    user.avatar_url=key
    try:
        db.session.commit()
    except Exception as e:
        current_app.logger.debug(e)
        return jsonify(re_code=RET.DBERR,msg='保存头像失败')
    # 拼接头像地址，返回前端
    avatar_url=constants.QINIU_DOMIN_PREFIX+user.avatar_url
    return jsonify(re_code=RET.OK,msg='上传头像成功',avatar_url=avatar_url)

@api.route('/sessions')
def check_login():
    """用户判断用户是否登录的接口：方便前端工作
    1.获取session中的user_id,name
    :return: user_id,name
    """
    user_id=session.get('user_id')
    name=session.get('name')

    return jsonify(re_code=RET.OK,msg='OK',user={'user_id':user_id,'name':name})