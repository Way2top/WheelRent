#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
订单数据模型
包含正式订单和临时预订单的数据结构和相关操作方法
"""

import uuid
from datetime import datetime, timedelta
from flask_sqlalchemy import SQLAlchemy

# 全局db变量，将在app.py中初始化
db = None

class FormalOrder(db.Model):
    """正式订单模型类"""
    
    __tablename__ = 'formal_order'
    
    # 字段定义
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_no = db.Column(db.String(50), unique=True, nullable=False, comment='订单号')
    user_name = db.Column(db.String(50), nullable=False, comment='用户姓名')
    user_phone = db.Column(db.String(20), nullable=False, comment='用户电话')
    user_address = db.Column(db.Text, nullable=False, comment='用户地址')
    wheelchair_id = db.Column(db.Integer, db.ForeignKey('wheelchair.id'), nullable=False, comment='轮椅ID')
    deposit = db.Column(db.Float, nullable=False, comment='定金')
    status = db.Column(db.String(20), nullable=False, default='待配送', comment='订单状态')
    create_time = db.Column(db.DateTime, default=datetime.utcnow, comment='创建时间')
    
    # 订单状态常量
    STATUS_PENDING = '待配送'
    STATUS_DELIVERING = '配送中'
    STATUS_COMPLETED = '已完成'
    STATUS_CANCELLED = '已取消'
    
    VALID_STATUSES = [STATUS_PENDING, STATUS_DELIVERING, STATUS_COMPLETED, STATUS_CANCELLED]
    
    def __init__(self, user_name, user_phone, user_address, wheelchair_id, deposit):
        """初始化正式订单对象"""
        self.order_no = self.generate_order_no()
        self.user_name = user_name
        self.user_phone = user_phone
        self.user_address = user_address
        self.wheelchair_id = wheelchair_id
        self.deposit = deposit
        self.status = self.STATUS_PENDING
        self.create_time = datetime.utcnow()
    
    def to_dict(self):
        """转换为字典格式"""
        return {
            'id': self.id,
            'order_no': self.order_no,
            'user_name': self.user_name,
            'user_phone': self.user_phone,
            'user_address': self.user_address,
            'wheelchair_id': self.wheelchair_id,
            'wheelchair_name': self.wheelchair.name if self.wheelchair else None,
            'deposit': self.deposit,
            'status': self.status,
            'create_time': self.create_time.strftime('%Y-%m-%d %H:%M:%S') if self.create_time else None
        }
    
    @staticmethod
    def generate_order_no():
        """生成订单号"""
        now = datetime.now()
        timestamp = now.strftime('%Y%m%d%H%M%S')
        random_suffix = str(uuid.uuid4())[:6].upper()
        return f'WR{timestamp}{random_suffix}'
    
    def update_status(self, new_status):
        """更新订单状态"""
        if new_status in self.VALID_STATUSES:
            old_status = self.status
            self.status = new_status
            return True, f'订单状态从 {old_status} 更新为 {new_status}'
        return False, f'无效的订单状态: {new_status}'
    
    def can_cancel(self):
        """检查订单是否可以取消"""
        return self.status in [self.STATUS_PENDING, self.STATUS_DELIVERING]
    
    def cancel(self):
        """取消订单"""
        if self.can_cancel():
            self.status = self.STATUS_CANCELLED
            return True
        return False
    
    @classmethod
    def get_by_status(cls, status, page=1, limit=10):
        """根据状态获取订单列表"""
        query = cls.query.filter(cls.status == status)
        total = query.count()
        orders = query.order_by(cls.create_time.desc()).offset((page - 1) * limit).limit(limit).all()
        return orders, total
    
    @classmethod
    def get_all(cls, page=1, limit=10, status_filter=None):
        """获取所有订单"""
        query = cls.query
        if status_filter:
            query = query.filter(cls.status == status_filter)
        
        total = query.count()
        orders = query.order_by(cls.create_time.desc()).offset((page - 1) * limit).limit(limit).all()
        return orders, total
    
    def __repr__(self):
        return f'<FormalOrder {self.order_no}: {self.user_name}>'


class TempOrder(db.Model):
    """临时预订单模型类"""
    
    __tablename__ = 'temp_order'
    
    # 字段定义
    id = db.Column(db.String(50), primary_key=True, comment='预订单ID')
    user_name = db.Column(db.String(50), comment='用户姓名')
    user_phone = db.Column(db.String(20), comment='用户电话')
    user_address = db.Column(db.Text, comment='用户地址')
    wheelchair_id = db.Column(db.Integer, comment='轮椅ID')
    create_time = db.Column(db.DateTime, default=datetime.utcnow, comment='创建时间')
    
    # 预订单过期时间（分钟）
    EXPIRE_MINUTES = 30
    
    def __init__(self, user_name, user_phone, user_address, wheelchair_id):
        """初始化临时预订单对象"""
        self.id = str(uuid.uuid4())
        self.user_name = user_name
        self.user_phone = user_phone
        self.user_address = user_address
        self.wheelchair_id = wheelchair_id
        self.create_time = datetime.utcnow()
    
    def to_dict(self):
        """转换为字典格式"""
        return {
            'id': self.id,
            'user_name': self.user_name,
            'user_phone': self.user_phone,
            'user_address': self.user_address,
            'wheelchair_id': self.wheelchair_id,
            'create_time': self.create_time.strftime('%Y-%m-%d %H:%M:%S') if self.create_time else None,
            'expire_time': self.get_expire_time().strftime('%Y-%m-%d %H:%M:%S')
        }
    
    def get_expire_time(self):
        """获取过期时间"""
        return self.create_time + timedelta(minutes=self.EXPIRE_MINUTES)
    
    def is_expired(self):
        """检查是否已过期"""
        return datetime.utcnow() > self.get_expire_time()
    
    def to_formal_order(self, deposit):
        """转换为正式订单"""
        if self.is_expired():
            return None, '预订单已过期'
        
        formal_order = FormalOrder(
            user_name=self.user_name,
            user_phone=self.user_phone,
            user_address=self.user_address,
            wheelchair_id=self.wheelchair_id,
            deposit=deposit
        )
        
        return formal_order, '转换成功'
    
    @classmethod
    def cleanup_expired(cls):
        """清理过期的临时订单"""
        expire_time = datetime.utcnow() - timedelta(minutes=cls.EXPIRE_MINUTES)
        expired_orders = cls.query.filter(cls.create_time < expire_time).all()
        
        for order in expired_orders:
            db.session.delete(order)
        
        db.session.commit()
        return len(expired_orders)
    
    @classmethod
    def get_by_id(cls, temp_order_id):
        """根据ID获取临时订单"""
        return cls.query.filter(cls.id == temp_order_id).first()
    
    def __repr__(self):
        return f'<TempOrder {self.id}: {self.user_name}>'