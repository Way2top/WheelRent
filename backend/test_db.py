#!/usr/bin/env python3
from app_simple import app, AdminUser, Wheelchair

with app.app_context():
    print("=== 用户数据 ===")
    users = AdminUser.query.all()
    for user in users:
        print(f"ID: {user.id}, Username: {user.username}, Role: {user.role}")
        # 测试密码验证
        result = user.check_password('123456')
        print(f"密码验证结果: {result}")
    
    print("\n=== 轮椅数据 ===")
    wheelchairs = Wheelchair.query.all()
    for wheelchair in wheelchairs:
        print(f"ID: {wheelchair.id}, Name: {wheelchair.name}, Price: {wheelchair.price}, Stock: {wheelchair.stock}")