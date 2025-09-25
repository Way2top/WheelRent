#!/usr/bin/env python3
from app_simple import app, AdminUser
from flask_jwt_extended import create_access_token, decode_token

with app.app_context():
    # 测试JWT令牌创建和解析
    user = AdminUser.query.filter_by(username='admin').first()
    print(f"User ID: {user.id}, Type: {type(user.id)}")
    
    # 测试不同的identity类型
    token1 = create_access_token(identity=user.id)
    token2 = create_access_token(identity=str(user.id))
    
    print(f"Token with int identity: {token1[:50]}...")
    print(f"Token with str identity: {token2[:50]}...")
    
    # 解析令牌
    try:
        decoded1 = decode_token(token1)
        print(f"Decoded token1 sub: {decoded1['sub']}, type: {type(decoded1['sub'])}")
    except Exception as e:
        print(f"Error decoding token1: {e}")
    
    try:
        decoded2 = decode_token(token2)
        print(f"Decoded token2 sub: {decoded2['sub']}, type: {type(decoded2['sub'])}")
    except Exception as e:
        print(f"Error decoding token2: {e}")