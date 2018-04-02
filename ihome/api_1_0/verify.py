# --*-- coding:utf-8 --*--
import re

from ihome import redis_conn, constants
from ihome.utils.captcha.captcha import captcha
from flask import current_app, jsonify, request, make_response, abort
from ihome.utils.response_code import RET,error_map
from ihome.api_1_0 import api

@api.route('/imageCode')
def get_image_code():
    """
    获取图片验证码
    1.接收请求，获取UUID和上一个uuid
    2.判断数据库保存的uuid是否等于last_uuid等于删除，
    3.生成图片验证码
    4.保存新的uuid，对应的图片文本信息
    :return: josnify 验证码图片
    """
    # 1.接收请求，获取UUID，last_uuid
    uuid=request.args.get('uuid')
    last_uuid=request.args.get('last_uuid')
    if not uuid:
        #缺省参数报403异常
        abort(403)
    # 2.生成图片验证码 名字，文字信息，图片信息
    name, text, image = captcha.generate_captcha()
    current_app.logger.debug('图片验证码信息：'+text)
    # 4.删除上次生成的验证码图片
    try:
        if last_uuid:
            redis_conn.delete('ImageCode:'+last_uuid)
        # 3.保存UUID对应的验证码文字信息,设置时长
        redis_conn.set('ImageCode:' + uuid, text,constants.IMAGE_CODE_REDIS_EXPIRES)
    except Exception as e:
        current_app.logger.debug(e)
        return jsonify(re_code=RET.DBERR,msg='保存图片验证码失败')
    response=make_response(image)
    response.headers['Content-Type']='image/jpg'
    return response

