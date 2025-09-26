#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据库初始化脚本
创建数据表并插入初始数据
"""

import os
import sys
import bcrypt
from datetime import datetime

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app_simple import app, db, Wheelchair, AdminUser, FormalOrder

def init_database():
    """初始化数据库"""
    with app.app_context():
        # 删除所有表
        db.drop_all()
        print("已删除所有数据表")
        
        # 创建所有表
        db.create_all()
        print("已创建所有数据表")
        
        # 创建管理员用户
        create_admin_users()
        
        # 创建轮椅数据
        create_wheelchairs()
        
        # 创建示例订单
        create_sample_orders()
        
        print("数据库初始化完成！")

def create_admin_users():
    """创建管理员用户"""
    # 创建默认管理员
    password = "admin123"
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    admin = AdminUser(
        username="admin",
        password_hash=password_hash,
        role="admin"
    )
    
    db.session.add(admin)
    db.session.commit()
    print(f"已创建管理员用户: admin / {password}")

def create_wheelchairs():
    """创建轮椅数据"""
    wheelchairs = [
        {
            "name": "电动轮椅豪华版",
            "description": "配备GPS定位、智能刹车系统的高端电动轮椅，适合长期使用",
            "price": 200.0,
            "stock": 3,
            "manufacturer": "智能康复设备有限公司"
        },
        {
            "name": "手动轮椅标准版",
            "description": "轻便耐用的手动轮椅，适合日常使用，操作简单",
            "price": 80.0,
            "stock": 5,
            "manufacturer": "康复器械制造厂"
        },
        {
            "name": "电动轮椅经济版",
            "description": "性价比高的电动轮椅，操作简单，续航能力强",
            "price": 120.0,
            "stock": 4,
            "manufacturer": "医疗设备公司"
        },
        {
            "name": "轻便折叠轮椅",
            "description": "超轻便设计，可快速折叠，方便携带和存储",
            "price": 100.0,
            "stock": 6,
            "manufacturer": "便携医疗器械厂"
        },
        {
            "name": "运动型轮椅",
            "description": "专为运动设计的轮椅，轻量化材质，操控性强",
            "price": 150.0,
            "stock": 2,
            "manufacturer": "运动康复设备公司"
        }
    ]
    
    for wheelchair_data in wheelchairs:
        wheelchair = Wheelchair(**wheelchair_data)
        db.session.add(wheelchair)
    
    db.session.commit()
    print(f"已创建 {len(wheelchairs)} 个轮椅记录")

def create_sample_orders():
    """创建示例订单"""
    orders = [
        {
            "order_no": "WR20250915001",
            "user_name": "张三",
            "user_phone": "13800138001",
            "user_address": "北京市朝阳区某某街道123号",
            "wheelchair_id": 1,
            "deposit": 200.0,
            "status": "使用中",
            "create_time": datetime(2025, 9, 15, 10, 30)
        },
        {
            "order_no": "WR20250914002",
            "user_name": "李四",
            "user_phone": "13800138002",
            "user_address": "上海市浦东新区某某路456号",
            "wheelchair_id": 2,
            "deposit": 80.0,
            "status": "已归还",
            "create_time": datetime(2025, 9, 14, 14, 20)
        },
        {
            "order_no": "WR20250913003",
            "user_name": "王五",
            "user_phone": "13800138003",
            "user_address": "广州市天河区某某大道789号",
            "wheelchair_id": 3,
            "deposit": 120.0,
            "status": "待配送",
            "create_time": datetime(2025, 9, 13, 16, 45)
        }
    ]
    
    for order_data in orders:
        order = FormalOrder(**order_data)
        db.session.add(order)
    
    db.session.commit()
    print(f"已创建 {len(orders)} 个示例订单")

def show_admin_info():
    """显示管理员信息"""
    with app.app_context():
        admin = AdminUser.query.filter_by(username="admin").first()
        if admin:
            print("\n=== 管理员登录信息 ===")
            print(f"用户名: {admin.username}")
            print(f"密码: admin123")
            print(f"角色: {admin.role}")
            print("========================\n")
        else:
            print("未找到管理员用户")

if __name__ == '__main__':
    print("开始初始化数据库...")
    init_database()
    show_admin_info()
    
    print("\n=== 系统信息 ===")
    print("后端服务地址: http://localhost:5001")
    print("客户端地址: http://localhost:5173")
    print("管理端地址: http://localhost:5174")
    print("健康检查: http://localhost:5001/health")
    print("API文档: http://localhost:5001/api")
    print("================\n")