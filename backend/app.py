#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
在线轮椅租赁系统 - Flask后端应用
主应用文件，包含应用初始化、配置和路由注册
"""

import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from datetime import timedelta

# 创建Flask应用实例
app = Flask(__name__)

# 应用配置
app.config['SECRET_KEY'] = 'wheelchair-rental-system-secret-key-2025'
app.config['JWT_SECRET_KEY'] = 'jwt-secret-string-wheelchair-rental'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)

# 数据库配置
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "wheelchair_rental.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 初始化扩展
db = SQLAlchemy(app)
jwt = JWTManager(app)
CORS(app, origins=['http://localhost:3000', 'http://localhost:5173', 'http://localhost:8080'])

# 导入路由（延迟导入模型避免循环依赖）
from routes.client_api import client_bp
from routes.admin_api import admin_bp

# 注册蓝图将在init_database后调用

# 全局错误处理
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'code': 404,
        'message': '请求的资源不存在'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'code': 500,
        'message': '服务器内部错误'
    }), 500

# JWT错误处理
@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify({
        'code': 401,
        'message': '令牌已过期，请重新登录'
    }), 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({
        'code': 401,
        'message': '无效的令牌'
    }), 401

@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({
        'code': 401,
        'message': '需要提供访问令牌'
    }), 401

# 健康检查接口
@app.route('/health')
def health_check():
    return jsonify({
        'code': 200,
        'message': '服务运行正常',
        'data': {
            'service': '在线轮椅租赁系统',
            'version': '1.0.0',
            'status': 'healthy'
        }
    })

# 根路径
@app.route('/')
def index():
    return jsonify({
        'code': 200,
        'message': '欢迎使用在线轮椅租赁系统API',
        'data': {
            'service': '在线轮椅租赁系统',
            'version': '1.0.0',
            'endpoints': {
                'client_api': '/api',
                'admin_api': '/api/admin',
                'health': '/health'
            }
        }
    })

# 初始化数据库
def init_database():
    """初始化数据库表结构"""
    with app.app_context():
        # 导入数据模型
        from models.wheelchair import Wheelchair
        from models.order import FormalOrder, TempOrder
        from models.user import AdminUser
        from models.log import OperationLog
        
        # 创建所有表
        db.create_all()
        print("数据库表创建完成")
        
        # 检查是否需要初始化数据
        if AdminUser.query.count() == 0:
            print("正在初始化基础数据...")
            print("请运行 database/init_sqlite.sql 脚本来初始化数据")

if __name__ == '__main__':
    # 初始化数据库
    init_database()
    
    # 启动应用
    print("正在启动在线轮椅租赁系统后端服务...")
    print("客户端API: http://localhost:5000/api")
    print("管理端API: http://localhost:5000/api/admin")
    print("健康检查: http://localhost:5000/health")
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )