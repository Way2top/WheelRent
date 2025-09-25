#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
用户数据模型
定义管理用户的数据结构和相关操作方法
"""

import bcrypt
from flask_sqlalchemy import SQLAlchemy

# 全局db变量，将在app.py中初始化
db = None

class AdminUser(db.Model):
    """管理用户模型类"""
    
    __tablename__ = 'admin_user'
    
    # 字段定义
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False, comment='用户名')
    password_hash = db.Column(db.String(255), nullable=False, comment='密码哈希')
    role = db.Column(db.String(20), nullable=False, comment='角色')
    is_deleted = db.Column(db.Boolean, default=False, comment='是否逻辑删除')
    
    # 角色常量
    ROLE_ADMIN = 'admin'
    ROLE_OPERATOR = 'operator'
    
    VALID_ROLES = [ROLE_ADMIN, ROLE_OPERATOR]
    
    # 关系定义
    operation_logs = db.relationship('OperationLog', backref='operator', lazy=True)
    
    def __init__(self, username, password, role):
        """初始化管理用户对象"""
        self.username = username
        self.set_password(password)
        self.role = role
        self.is_deleted = False
    
    def to_dict(self, include_sensitive=False):
        """转换为字典格式"""
        data = {
            'id': self.id,
            'username': self.username,
            'role': self.role,
            'is_deleted': self.is_deleted
        }
        
        if include_sensitive:
            data['password_hash'] = self.password_hash
        
        return data
    
    def set_password(self, password):
        """设置密码（自动加密）"""
        if isinstance(password, str):
            password = password.encode('utf-8')
        
        salt = bcrypt.gensalt()
        self.password_hash = bcrypt.hashpw(password, salt).decode('utf-8')
    
    def check_password(self, password):
        """验证密码"""
        if isinstance(password, str):
            password = password.encode('utf-8')
        
        if isinstance(self.password_hash, str):
            password_hash = self.password_hash.encode('utf-8')
        else:
            password_hash = self.password_hash
        
        return bcrypt.checkpw(password, password_hash)
    
    def is_admin(self):
        """检查是否为管理员"""
        return self.role == self.ROLE_ADMIN
    
    def is_operator(self):
        """检查是否为操作员"""
        return self.role == self.ROLE_OPERATOR
    
    def can_manage_users(self):
        """检查是否可以管理用户"""
        return self.is_admin()
    
    def can_manage_inventory(self):
        """检查是否可以管理库存"""
        return self.role in [self.ROLE_ADMIN, self.ROLE_OPERATOR]
    
    def can_manage_orders(self):
        """检查是否可以管理订单"""
        return self.role in [self.ROLE_ADMIN, self.ROLE_OPERATOR]
    
    def soft_delete(self):
        """逻辑删除用户"""
        self.is_deleted = True
    
    def restore(self):
        """恢复已删除的用户"""
        self.is_deleted = False
    
    def update_role(self, new_role):
        """更新用户角色"""
        if new_role in self.VALID_ROLES:
            old_role = self.role
            self.role = new_role
            return True, f'角色从 {old_role} 更新为 {new_role}'
        return False, f'无效的角色: {new_role}'
    
    @classmethod
    def authenticate(cls, username, password):
        """用户认证
        
        Args:
            username: 用户名
            password: 密码
        
        Returns:
            tuple: (用户对象, 认证结果消息)
        """
        user = cls.query.filter(
            cls.username == username,
            cls.is_deleted == False
        ).first()
        
        if not user:
            return None, '用户不存在'
        
        if user.check_password(password):
            return user, '认证成功'
        else:
            return None, '密码错误'
    
    @classmethod
    def get_by_username(cls, username, include_deleted=False):
        """根据用户名获取用户"""
        query = cls.query.filter(cls.username == username)
        if not include_deleted:
            query = query.filter(cls.is_deleted == False)
        return query.first()
    
    @classmethod
    def get_by_id(cls, user_id, include_deleted=False):
        """根据ID获取用户"""
        query = cls.query.filter(cls.id == user_id)
        if not include_deleted:
            query = query.filter(cls.is_deleted == False)
        return query.first()
    
    @classmethod
    def get_all(cls, page=1, limit=10, include_deleted=False, role_filter=None):
        """获取所有用户"""
        query = cls.query
        
        if not include_deleted:
            query = query.filter(cls.is_deleted == False)
        
        if role_filter:
            query = query.filter(cls.role == role_filter)
        
        total = query.count()
        users = query.order_by(cls.id.desc()).offset((page - 1) * limit).limit(limit).all()
        return users, total
    
    @classmethod
    def username_exists(cls, username, exclude_id=None):
        """检查用户名是否已存在"""
        query = cls.query.filter(
            cls.username == username,
            cls.is_deleted == False
        )
        
        if exclude_id:
            query = query.filter(cls.id != exclude_id)
        
        return query.first() is not None
    
    @classmethod
    def create_user(cls, username, password, role):
        """创建新用户
        
        Args:
            username: 用户名
            password: 密码
            role: 角色
        
        Returns:
            tuple: (用户对象, 创建结果消息)
        """
        # 验证角色
        if role not in cls.VALID_ROLES:
            return None, f'无效的角色: {role}'
        
        # 检查用户名是否已存在
        if cls.username_exists(username):
            return None, '用户名已存在'
        
        # 创建用户
        try:
            user = cls(username=username, password=password, role=role)
            db.session.add(user)
            db.session.commit()
            return user, '用户创建成功'
        except Exception as e:
            db.session.rollback()
            return None, f'用户创建失败: {str(e)}'
    
    def __repr__(self):
        return f'<AdminUser {self.id}: {self.username} ({self.role})>'