# --*-- coding:utf-8 --*--
from flask import current_app, jsonify, request, g, session

from ihome import db, constants
from ihome.api_1_0 import api
from ihome.models import Area, House, Facility, HouseImage
from ihome.utils.common import login_required
from ihome.utils.qiniu_image_storage import upload_image
from ihome.utils.response_code import RET

@api.route('/areas')
def get_areas():
    """获取城区信息：
    1.查询出所有城区信息
    2.响应数据
    """
    # 1.查询所有城区信息
    try:
        areas=Area.query.all()
    except Exception as e:
        current_app.logger.debug(e)
        return jsonify(re_code=RET.DBERR,msg='查询城区信息失败')

    if not areas:
        return jsonify(re_code=RET.NODATA,msg='暂无城区')

    areas=[area.to_dict() for area in areas]
    return jsonify(re_code=RET.OK,msg='查询城区成功',areas=areas)

@api.route('/houses',methods=['POST'])
@login_required
def pub_house():
    """发布房源：
    0.登录校验  @login_required
    1.g中获取user_id，前端获取房屋信息并校验数据
    2.保存数据到数据库
    3.返回响应
    """
    #1.前端获取房屋信息并校验数据
    json_dict=request.json
    """
    {u'area_id': u'1',u'capacity': u'1',u'title': u'1',u'price': u'1', u'facility': [u'1', u'3', u'5'],
    u'acreage': u'1',u'beds': u'1',u'room_count': u'1', u'max_days': u'1',u'deposit': u'1',
    u'address': u'11', u'min_days': u'1',u'unit': u'1'}
    """
    area_id=json_dict.get('area_id')
    capacity = json_dict.get('capacity')
    title = json_dict.get('title')
    price = json_dict.get('price')
    facilities = json_dict.get('facility')
    acreage = json_dict.get('acreage')
    beds = json_dict.get('beds')
    room_count = json_dict.get('room_count')
    max_days = json_dict.get('max_days')
    deposit = json_dict.get('deposit')
    address = json_dict.get('address')
    min_days = json_dict.get('min_days')
    unit = json_dict.get('unit')
    if not all([unit,min_days,max_days,address,deposit,room_count,beds,acreage,facilities,price,title,capacity,area_id]):
        return jsonify(re_code=RET.PARAMERR,msg='参数不完整')

    try:
        price=int(float(price)*100)
        deposit=int(float(deposit)*100)
    except Exception as e:
        current_app.logger.debug(e)
        return jsonify(re_code=RET.PARAMERR,msg='数据格式错误')

    #2.保存数据到数据库
    house=House()
    house.area_id=area_id
    house.user_id=g.user_id
    house.title=title
    house.price=price
    house.address=address
    house.room_count=room_count
    house.acreage=acreage
    house.unit=unit
    house.beds=beds
    house.deposit=deposit
    house.min_days=min_days
    house.max_days=max_days
    house.facilities=Facility.query.filter(Facility.id.in_(facilities)).all()

    try:
        db.session.add(house)
        db.session.commit()
    except Exception as e:
        current_app.logger.debug(e)
        db.session.rollback()
        return jsonify(re_code=RET.DBERR,msg='新增房屋失败')
    #3.返回响应house_id
    return jsonify(re_code=RET.OK,msg='发布房源成功',data={'house_id':house.id})

@api.route('/houses/<int:house_id>/images',methods=['POST'])
@login_required
def upload_house_image(house_id):
    """上传房屋图片：
    0.登录校验 @login_required
    1.获取图片信息
    2.上传到七牛云,返回key
    #3.查询当前房屋是否有房屋主图片，没有就为其添加
    #4.添加数据到当前house_id的House_Image模型中
    #5.响应数据
    """
    #1.获取图片信息
    house_image = request.files.get('house_image')
    if not house_image:
        return jsonify(re_code=RET.PARAMERR,msg='图片不能为空')
    #2.上传到七牛云,返回key
    try:
        key=upload_image(house_image)
    except Exception as e:
        current_app.logger.debug(e)
        return jsonify(re_code=RET.THIRDERR,msg='上传房屋图片失败')
    #3.查询当前房屋是否有房屋主图片，没有就为其添加
    try:
        house=House.query.get(house_id)
    except Exception as e:
        current_app.logger.debug(e)
        return jsonify(re_code=RET.DBERR,msg='查询房屋失败')
    if not house:
        return jsonify(re_code=RET.NODATA,msg='无该房屋')
    if not house.index_image_url:
        house.index_image_url=key
    #4.添加数据到当前house_id的House_Image模型中
    house_image=HouseImage()
    house_image.house_id=house_id
    house_image.url=key
    try:
        db.session.add(house_image)
        db.session.commit()
    except Exception as e:
        current_app.logger.debug(e)
        db.session.rollback()
        return jsonify(re_code=RET.DBERR,msg='保存房屋图片失败')
    #5.响应数据
    return jsonify(re_code=RET.OK,msg='上传图片成功',data={'url':constants.QINIU_DOMIN_PREFIX+key})

# @api.route('/')
# def search_houses():
#     """根据查询条件查询房屋信息并分页：search.html?aid=&aname=&sd=&ed=
#
#     """
@api.route('/houses/index')
def houses_index():
    """首页房屋推荐：
    1.获取新上架的5个房源基本信息
    2.返回响应
    """
    # 1.获取新上架的5个房源基本信息
    houses=None
    try:
        houses=House.query.order_by(House.create_time.desc()).limit(constants.HOME_PAGE_MAX_HOUSES)
    except Exception as e:
        current_app.logger.debug(e)
    if not houses:
        return jsonify(re_code=RET.NODATA,msg='无房屋信息')
    houses=[house.to_basic_dict() for house in houses]
    #2.返回响应
    return jsonify(re_code=RET.OK,msg='查询房屋成功',data={'houses':houses})

@api.route('/houses/detail/<int:house_id>')
def house_detail(house_id):
    """房屋详情页面：
    1.获取url栏中的house_id
    2.根据house_id获取house详细信息
    3.判断用户是否登录，
    4.响应结果
    """
    #1.获取url栏中的house_id
    #2.根据house_id获取house详细信息
    try:
        house=House.query.get(house_id)
    except Exception as e:
        current_app.logger.debug(e)
        return jsonify(re_code=RET.DBERR,msg='查询房屋信息失败')
    if not house:
        return jsonify(re_code=RET.NODATA,msg='房屋不存在')
    house=house.to_full_dict()
    # 3. 获取user_id : 当用户登录后访问detail.html，就会有user_id，反之，没有user_id
    login_user_id=session.get('user_id',-1)
    #4.响应结果
    return jsonify(re_code=RET.OK,msg='查询成功',data={'house':house,'login_user_id':login_user_id})

@api.route('/users/houses')
@login_required
def my_houses():
    """我的房源列表接口：
    0.登录校验 @login_required
    1.获取登录用户的所有发布的房源
    2.响应数据
    """
    #1.获取登录用户的所有发布的房源
    try:
        houses=House.query.filter(House.user_id==g.user_id)
    except Exception as e:
        current_app.logger.debug(e)
        return jsonify(re_code=RET.DBERR,msg='查询房屋失败')

    #2.响应数据
    houses=[house.to_basic_dict() for house in houses]
    return jsonify(re_code=RET.OK,msg='查询成功',data={'houses':houses})