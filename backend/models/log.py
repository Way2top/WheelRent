#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
操作日志数据模型
定义操作日志的数据结构和相关操作方法
"""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

# 从app.py导入db实例
from app import db

class OperationLog(db.Model):
    """操作日志模型类"""
    
    __tablename__ = 'operation_log'
    
    # 字段定义
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    operator_id = db.Column(db.Integer, db.ForeignKey('admin_user.id'), nullable=False, comment='操作员ID')
    operate_type = db.Column(db.String(50), nullable=False, comment='操作类型')
    target_id = db.Column(db.Integer, comment='操作对象ID')
    operate_time = db.Column(db.DateTime, default=datetime.utcnow, comment='操作时间')
    
    # 操作类型常量
    TYPE_ADD_WHEELCHAIR = '新增轮椅'
    TYPE_UPDATE_WHEELCHAIR = '修改轮椅'
    TYPE_DELETE_WHEELCHAIR = '删除轮椅'
    TYPE_OFFLINE_WHEELCHAIR = '下架轮椅'
    TYPE_ONLINE_WHEELCHAIR = '上架轮椅'
    TYPE_UPDATE_STOCK = '更新库存'
    
    TYPE_UPDATE_ORDER_STATUS = '修改订单状态'
    TYPE_CANCEL_ORDER = '取消订单'
    
    TYPE_ADD_USER = '新增用户'
    TYPE_UPDATE_USER = '修改用户'
    TYPE_DELETE_USER = '删除用户'
    TYPE_UPDATE_USER_ROLE = '修改用户角色'
    
    TYPE_LOGIN = '用户登录'
    TYPE_LOGOUT = '用户登出'
    
    # 所有有效的操作类型
    VALID_TYPES = [
        TYPE_ADD_WHEELCHAIR, TYPE_UPDATE_WHEELCHAIR, TYPE_DELETE_WHEELCHAIR,
        TYPE_OFFLINE_WHEELCHAIR, TYPE_ONLINE_WHEELCHAIR, TYPE_UPDATE_STOCK,
        TYPE_UPDATE_ORDER_STATUS, TYPE_CANCEL_ORDER,
        TYPE_ADD_USER, TYPE_UPDATE_USER, TYPE_DELETE_USER, TYPE_UPDATE_USER_ROLE,
        TYPE_LOGIN, TYPE_LOGOUT
    ]
    
    def __init__(self, operator_id, operate_type, target_id=None):
        """初始化操作日志对象"""
        self.operator_id = operator_id
        self.operate_type = operate_type
        self.target_id = target_id
        self.operate_time = datetime.utcnow()
    
    def to_dict(self):
        """转换为字典格式"""
        return {
            'id': self.id,
            'operator_id': self.operator_id,
            'operator_name': self.operator.username if self.operator else None,
            'operator_role': self.operator.role if self.operator else None,
            'operate_type': self.operate_type,
            'target_id': self.target_id,
            'operate_time': self.operate_time.strftime('%Y-%m-%d %H:%M:%S') if self.operate_time else None
        }
    
    @classmethod
    def log_operation(cls, operator_id, operate_type, target_id=None):
        """记录操作日志
        
        Args:
            operator_id: 操作员ID
            operate_type: 操作类型
            target_id: 操作对象ID（可选）
        
        Returns:
            bool: 是否记录成功
        """
        try:
            if operate_type not in cls.VALID_TYPES:
                print(f"警告: 无效的操作类型 {operate_type}")
                return False
            
            log = cls(
                operator_id=operator_id,
                operate_type=operate_type,
                target_id=target_id
            )
            
            db.session.add(log)
            db.session.commit()
            return True
        except Exception as e:
            print(f"记录操作日志失败: {str(e)}")
            db.session.rollback()
            return False
    
    @classmethod
    def get_logs(cls, page=1, limit=20, operator_id=None, operate_type=None, start_date=None, end_date=None):
        """获取操作日志列表
        
        Args:
            page: 页码
            limit: 每页数量
            operator_id: 操作员ID过滤
            operate_type: 操作类型过滤
            start_date: 开始日期
            end_date: 结束日期
        
        Returns:
            tuple: (日志列表, 总数量)
        """
        query = cls.query
        
        # 操作员过滤
        if operator_id:
            query = query.filter(cls.operator_id == operator_id)
        
        # 操作类型过滤
        if operate_type:
            query = query.filter(cls.operate_type == operate_type)
        
        # 日期范围过滤
        if start_date:
            query = query.filter(cls.operate_time >= start_date)
        if end_date:
            query = query.filter(cls.operate_time <= end_date)
        
        # 按时间倒序排列
        query = query.order_by(cls.operate_time.desc())
        
        # 分页
        total = query.count()
        logs = query.offset((page - 1) * limit).limit(limit).all()
        
        return logs, total
    
    @classmethod
    def get_operator_logs(cls, operator_id, page=1, limit=20):
        """获取指定操作员的日志"""
        return cls.get_logs(page=page, limit=limit, operator_id=operator_id)
    
    @classmethod
    def get_logs_by_type(cls, operate_type, page=1, limit=20):
        """获取指定类型的日志"""
        return cls.get_logs(page=page, limit=limit, operate_type=operate_type)
    
    @classmethod
    def get_recent_logs(cls, limit=10):
        """获取最近的操作日志"""
        logs = cls.query.order_by(cls.operate_time.desc()).limit(limit).all()
        return logs
    
    @classmethod
    def get_statistics(cls, start_date=None, end_date=None):
        """获取操作统计信息
        
        Args:
            start_date: 开始日期
            end_date: 结束日期
        
        Returns:
            dict: 统计信息
        """
        query = cls.query
        
        if start_date:
            query = query.filter(cls.operate_time >= start_date)
        if end_date:
            query = query.filter(cls.operate_time <= end_date)
        
        # 总操作数
        total_operations = query.count()
        
        # 按操作类型统计
        type_stats = {}
        for operate_type in cls.VALID_TYPES:
            count = query.filter(cls.operate_type == operate_type).count()
            if count > 0:
                type_stats[operate_type] = count
        
        # 按操作员统计
        operator_stats = {}
        operators = db.session.query(cls.operator_id, db.func.count(cls.id)).group_by(cls.operator_id).all()
        for operator_id, count in operators:
            operator_stats[operator_id] = count
        
        return {
            'total_operations': total_operations,
            'type_statistics': type_stats,
            'operator_statistics': operator_stats
        }
    
    def __repr__(self):
        return f'<OperationLog {self.id}: {self.operate_type} by {self.operator_id}>'