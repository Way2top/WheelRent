#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
轮椅数据模型
定义轮椅信息的数据结构和相关操作方法
"""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_

# 延迟导入避免循环依赖
db = None

def init_db(database):
    global db
    db = database

def get_db():
    """获取数据库实例"""
    from app import db as app_db
    return app_db

class Wheelchair:
    """轮椅模型类"""
    
    def __init__(self, name, price, description=None, stock=1, manufacturer=None):
        """初始化轮椅对象"""
        self.name = name
        self.price = price
        self.description = description
        self.stock = stock
        self.manufacturer = manufacturer
        self.is_offline = False
        self.is_deleted = False
    
    def to_dict(self):
        """转换为字典格式"""
        return {
            'id': getattr(self, 'id', None),
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'stock': self.stock,
            'manufacturer': self.manufacturer,
            'is_offline': self.is_offline,
            'is_deleted': self.is_deleted
        }
    
    def is_available(self):
        """检查轮椅是否可用（未下架、未删除、有库存）"""
        return not self.is_offline and not self.is_deleted and self.stock > 0
    
    def reduce_stock(self, quantity=1):
        """减少库存"""
        if self.stock >= quantity:
            self.stock -= quantity
            return True
        return False
    
    def increase_stock(self, quantity=1):
        """增加库存"""
        self.stock += quantity
    
    def set_offline(self):
        """设置为下架状态"""
        self.is_offline = True
    
    def set_online(self):
        """设置为上架状态"""
        self.is_offline = False
    
    def soft_delete(self):
        """逻辑删除"""
        self.is_deleted = True
    
    @classmethod
    def search(cls, keyword=None, sort_type=None, page=1, limit=10, include_offline=False):
        """搜索轮椅
        
        Args:
            keyword: 搜索关键词
            sort_type: 排序类型 (price_asc, price_desc)
            page: 页码
            limit: 每页数量
            include_offline: 是否包含下架商品
        
        Returns:
            tuple: (轮椅列表, 总数量)
        """
        db = get_db()
        WheelchairModel = get_wheelchair_model()
        
        query = WheelchairModel.query.filter(WheelchairModel.is_deleted == False)
        
        # 是否包含下架商品
        if not include_offline:
            query = query.filter(WheelchairModel.is_offline == False)
        
        # 关键词搜索
        if keyword:
            search_filter = or_(
                WheelchairModel.name.contains(keyword),
                WheelchairModel.description.contains(keyword),
                WheelchairModel.manufacturer.contains(keyword)
            )
            query = query.filter(search_filter)
        
        # 排序
        if sort_type == 'price_asc':
            query = query.order_by(WheelchairModel.price.asc())
        elif sort_type == 'price_desc':
            query = query.order_by(WheelchairModel.price.desc())
        else:
            query = query.order_by(WheelchairModel.id.desc())  # 默认按ID倒序
        
        # 分页
        total = query.count()
        wheelchairs = query.offset((page - 1) * limit).limit(limit).all()
        
        return wheelchairs, total
    
    @classmethod
    def get_available_by_id(cls, wheelchair_id):
        """根据ID获取可用的轮椅"""
        WheelchairModel = get_wheelchair_model()
        return WheelchairModel.query.filter(
            WheelchairModel.id == wheelchair_id,
            WheelchairModel.is_deleted == False,
            WheelchairModel.is_offline == False,
            WheelchairModel.stock > 0
        ).first()
    
    @classmethod
    def get_by_id(cls, wheelchair_id, include_deleted=False):
        """根据ID获取轮椅"""
        WheelchairModel = get_wheelchair_model()
        query = WheelchairModel.query.filter(WheelchairModel.id == wheelchair_id)
        if not include_deleted:
            query = query.filter(WheelchairModel.is_deleted == False)
        return query.first()
    
    def __repr__(self):
        return f'<Wheelchair {getattr(self, "id", "new")}: {self.name}>'

def get_wheelchair_model():
    """获取轮椅数据库模型"""
    db = get_db()
    
    class WheelchairModel(db.Model):
        """轮椅数据库模型类"""
        
        __tablename__ = 'wheelchair'
        
        # 字段定义
        id = db.Column(db.Integer, primary_key=True, autoincrement=True)
        name = db.Column(db.String(100), nullable=False, comment='轮椅名称')
        description = db.Column(db.Text, comment='轮椅描述')
        price = db.Column(db.Float, nullable=False, comment='租赁价格')
        stock = db.Column(db.Integer, nullable=False, default=1, comment='库存数量')
        manufacturer = db.Column(db.String(100), comment='制造商')
        is_offline = db.Column(db.Boolean, default=False, comment='是否下架')
        is_deleted = db.Column(db.Boolean, default=False, comment='是否逻辑删除')
        
        # 关系定义
        formal_orders = db.relationship('FormalOrder', backref='wheelchair', lazy=True)
        temp_orders = db.relationship('TempOrder', backref='wheelchair', lazy=True)
        
        def to_dict(self):
            """转换为字典格式"""
            return {
                'id': self.id,
                'name': self.name,
                'description': self.description,
                'price': self.price,
                'stock': self.stock,
                'manufacturer': self.manufacturer,
                'is_offline': self.is_offline,
                'is_deleted': self.is_deleted
            }
        
        def is_available(self):
            """检查轮椅是否可用（未下架、未删除、有库存）"""
            return not self.is_offline and not self.is_deleted and self.stock > 0
        
        def reduce_stock(self, quantity=1):
            """减少库存"""
            if self.stock >= quantity:
                self.stock -= quantity
                return True
            return False
        
        def increase_stock(self, quantity=1):
            """增加库存"""
            self.stock += quantity
        
        def set_offline(self):
            """设置为下架状态"""
            self.is_offline = True
        
        def set_online(self):
            """设置为上架状态"""
            self.is_offline = False
        
        def soft_delete(self):
            """逻辑删除"""
            self.is_deleted = True
    
    return WheelchairModel

# 为了向后兼容，创建一个别名
Wheelchair = get_wheelchair_model