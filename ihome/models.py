# --*-- coding:utf-8 --*--
from datetime import datetime
from . import db

class BaseModel(object):
    """模型基类"""
    create_time=db.Column(db.DateTime,default=datetime.now()) #记录模型类创建时间
    update_time=db.Column(db.DateTime,default=datetime.now,onupdate=datetime.now())#记录模型类更新时间

class User(BaseModel,db.Model):
    """用户模型类"""
    __tablename__='ih_user_profile'

    id=db.Column(db.Integer,primary_key=True)  # 用户编号
    name=db.Column(db.String(32),unique=True,nullable=False) #用户昵称
    password=db.Column(db.String(128),nullable=False) # 加密的密码
    phone_num=db.Column(db.String(11),unique=True,nullable=False) # 手机号
    real_name=db.Column(db.String(32))  # 真实姓名
    id_card=db.Column(db.String(20))  #身份证号
    avatar_url=db.Column(db.String(128)) # 用户头像路径
    houses=db.relationship('House',backref='user',lazy='dynamic') # 用户发布的房屋
    orders=db.relationship('Order',backref='user',lazy='dynamic') # 用户下的订单

class Area(BaseModel,db.Model):
    """城区"""
    __tablename__='ih_area_info'

    id=db.Column(db.Integer,primary_key=True) # 区域编号
    name=db.Column(db.String(32),nullable=False) #区域名字
    houses=db.relationship('House',backref='area') # 区域的房屋


class Facility(BaseModel,db.Model):
    """房屋设施信息模型类"""
    __tablename__='ih_facility_info'

    id=db.Column(db.Integer,primary_key=True) #设施编号
    name=db.Column(db.String(32),nullable=False) #设施名字

# 房屋设施表，建立房屋与设施的多对多关系
house_facility=db.Table(
    "ih_house_facility",
    db.Column('house_id',db.Integer,db.ForeignKey('ih_house_info.id'),primary_key=True), # 房屋编号
    db.Column('facility_id',db.Integer,db.ForeignKey('ih_facility_info.id'),primary_key=True) # 设施编号
)


class House(BaseModel,db.Model):
    """房屋模型类"""

    __tablename__='ih_house_info'

    id=db.Column(db.Integer,primary_key=True) # 房屋编号
    user_id=db.Column(db.Integer,db.ForeignKey('ih_user_profile.id'),nullable=False) # 房屋主人编号
    area_id=db.Column(db.Integer,db.ForeignKey('ih_area_info.id'),nullable=False) #房屋地区编号
    title=db.Column(db.String(64),nullable=False) # 标题
    price=db.Column(db.Numeric(precision=2)) # 单价 单位：分
    address=db.Column(db.String(512),default='') # 地址
    room_count=db.Column(db.Integer,default=1) #房间数目
    acreage=db.Column(db.Integer,default=0) # 房间面积
    unit=db.Column(db.String(32),default='') # 房屋单元,几室几厅
    beds = db.Column(db.String(64), default="")  # 房屋床铺的配置
    deposit = db.Column(db.Integer, default=0)  # 房屋押金
    min_days = db.Column(db.Integer, default=1)  # 最少入住天数
    max_days = db.Column(db.Integer, default=0)  # 最多入住天数，0表示不限制
    order_count = db.Column(db.Integer, default=0)  # 预订完成的该房屋的订单数
    index_image_url = db.Column(db.String(256), default="")  # 房屋主图片的路径
    facilities = db.relationship("Facility", secondary=house_facility)  # 房屋的设施
    images = db.relationship("HouseImage")  # 房屋的图片
    orders = db.relationship("Order", backref="house")  # 房屋的订单


class HouseImage(BaseModel,db.Model):
    """房屋图片模型类"""
    __tablename__='ih_house_image'

    id=db.Column(db.Integer,primary_key=True)
    house_id=db.Column(db.Integer,db.ForeignKey('ih_house_info.id'),nullable=False)
    url=db.Column(db.String(256),nullable=False) #图片路径

class Order(BaseModel, db.Model):
    """订单"""

    __tablename__ = "ih_order_info"

    id = db.Column(db.Integer, primary_key=True)  # 订单编号
    user_id = db.Column(db.Integer, db.ForeignKey("ih_user_profile.id"), nullable=False)  # 下订单的用户编号
    house_id = db.Column(db.Integer, db.ForeignKey("ih_house_info.id"), nullable=False)  # 预订的房间编号
    begin_date = db.Column(db.DateTime, nullable=False)  # 预订的起始时间
    end_date = db.Column(db.DateTime, nullable=False)  # 预订的结束时间
    days = db.Column(db.Integer, nullable=False)  # 预订的总天数
    house_price = db.Column(db.Numeric(precision=2), nullable=False)  # 房屋的单价
    amount = db.Column(db.Numeric(precision=2), nullable=False)  # 订单的总金额
    status = db.Column(  # 订单的状态
        db.Enum(
            "WAIT_ACCEPT",  # 待接单,
            "WAIT_PAYMENT",  # 待支付
            "PAID",  # 已支付
            "WAIT_COMMENT",  # 待评价
            "COMPLETE",  # 已完成
            "CANCELED",  # 已取消
            "REJECTED"  # 已拒单
        ),
        default="WAIT_ACCEPT", index=True)
    comment = db.Column(db.Text)  # 订单的评论信息或者拒单原因
