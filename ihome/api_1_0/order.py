# --*-- coding:utf-8 --*--
from datetime import datetime
from flask import request, jsonify, current_app, g

from ihome import db
from ihome.api_1_0 import api
from ihome.models import Order, House
from ihome.utils.common import login_required
from ihome.utils.response_code import RET


@api.route('/orders',methods=['POST'])
@login_required
def create_order():
    """添加订单：
    0.登录校验
    1.获取请求参数,useri_id
    2.日期字符串转为日期对象，查询订单时间段是否和已有订单时间段冲突
    3.计算时间
    4.添加订单
    5.返回响应结果
    """
    # 1.获取参数{u'house_id': u'4', u'start_date': u'2018-04-10', u'end_date': u'2018-04-13'}
    json_dict=request.json
    house_id=json_dict.get('house_id')
    start_date = json_dict.get('start_date')
    end_date = json_dict.get('end_date')
   #校验数据
    if not all([house_id,start_date,end_date]):
        return jsonify(re_code=RET.PARAMERR,msg='参数有误')
    # 2.查询订单时间段是否和已有订单时间段冲突
    try:
        start_date=datetime.strptime(start_date,'%Y-%m-%d')
        end_date=datetime.strptime(end_date,'%Y-%m-%d')
    except Exception as e:
        current_app.logger.debug(e)
        return jsonify(re_code=RET.PARAMERR,msg='日期格式错误')

    #判断房屋是否存在
    try:
        house=House.query.get(house_id)
    except Exception as e:
        current_app.logger.debug(e)
        return jsonify(re_code=RET.DBERR,msg='查询房屋失败')
    if not house:
        return jsonify(re_code=RET.NODATA,msg='房屋不存在')
    #查询冲突房屋
    try:
        conflict_house=Order.query.filter(Order.house_id==house_id,Order.end_date>start_date,Order.begin_date<end_date).first()
    except Exception as e:
        current_app.logger.debug(e)
        return jsonify(re_code=RET.DBERR,msg='查询冲突房屋失败')
    if conflict_house:
        return jsonify(re_code=RET.DATAERR,msg='房屋已被预订')

    # 3.计算时间
    days=(end_date-start_date).days
    # 4.创建订单模型类
    order=Order()
    order.user_id=g.user_id
    order.house_id=house_id
    order.begin_date=start_date
    order.end_date=end_date
    order.days=days
    order.house_price=house.price
    order.amount=house.price*days
    try:
        db.session.add(order)
        db.session.commit()
    except Exception as e:
        current_app.logger.debug(e)
        return jsonify(re_code=RET.DBERR,msg='保存订单失败')

    # 5.返回响应结果
    return jsonify(re_code=RET.OK,msg='ok')

@api.route('/orders')
@login_required
def get_order_list():
    """根据url地址栏中的role字段判断查询的是我的订单还是客户订单：
    0.登录校验
    1. 获取参数role，user_id
    2.判断url中的role如果是customer返回客户订单数据，否则返回我的订单数据
    3.返回响应
    """
    # 1. 获取参数role，user_id
    role=request.args.get('role')
    if role not in['customer','own']:
        return jsonify(re_code=RET.PARAMERR,msg='参数错误')

    #2.判断url中的role如果是customer返回客户订单数据，否则返回我的订单数据
    try:
        if role=='customer':
            # 查询客户订单
            #2.1先查询自己发布的房源
            houses=House.query.filter(House.user_id==g.user_id).all()
            #2.2根据房源id查询所有订单
            house_ids=[house.id for house in houses]
            orders=Order.query.filter(Order.house_id.in_(house_ids)).all()
        else:
            # 查询自己的订单
            orders=Order.query.filter(Order.user_id==g.user_id).all()
    except Exception as e:
        current_app.logger.debug(e)
        return jsonify(re_code=RET.DBERR,msg='查询订单失败')
    # 2.3返回订单信息
    order_list = [order.to_dict() for order in orders]
    return jsonify(re_code=RET.OK,msg='查询成功',data={'order_list':order_list})

@api.route('/orders/status/<int:order_id>',methods=['PUT'])
@login_required
def set_order_status(order_id):
    """设置订单的状态：accept: 接单，reject：拒单
    0.登录校验  @login_required
    1.获取参数 action,如果是拒单需要接收拒单理由reason，user_id
    2.获取订单，设置相应订单状态
    3.返回响应
    """
    #1.获取参数action, 如果是拒单需要接收拒单理由reason，user_id
    action=request.args.get('action')
    user_id=g.user_id
    #校验参数
    if action not in ['accept','reject']:
        return jsonify(re_code=RET.PARAMERR,msg='参数错误')

    try:
        #2.获取订单，设置相应订单状态
        order=Order.query.get(order_id)
        if action=='accept':
            order.status='WAIT_PAYMENT'
        else:
            # 获取拒单理由
            reason=request.json.get('reason')
            if not reason:
                return jsonify(re_code=RET.PARAMERR,msg='拒绝理由不能为空')
            order.status='REJECTED'
            order.comment=reason
        db.session.commit()
    except Exception as e:
        current_app.logger.debug(e)
        db.session.rollback()
        return jsonify(re_code=RET.DBERR,msg='查询订单失败')

    #返回响应
    return jsonify(re_code=RET.OK,msg='提交成功')
