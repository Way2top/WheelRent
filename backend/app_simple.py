#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
在线轮椅租赁系统 - 简化版Flask后端应用
用于测试基本功能
"""

import os
import uuid
import bcrypt
from datetime import datetime, timedelta
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS
from sqlalchemy import or_

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
CORS(app, origins=['http://localhost:3000', 'http://localhost:5173', 'http://localhost:5174', 'http://localhost:5175', 'http://localhost:5176', 'http://localhost:8080'])

# 数据模型定义
class Wheelchair(db.Model):
    """轮椅模型"""
    __tablename__ = 'wheelchair'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=1)
    manufacturer = db.Column(db.String(100))
    is_offline = db.Column(db.Boolean, default=False)
    is_deleted = db.Column(db.Boolean, default=False)
    
    def to_dict(self):
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
    
    def reduce_stock(self, quantity=1):
        if self.stock >= quantity:
            self.stock -= quantity
            return True
        return False

class FormalOrder(db.Model):
    """正式订单模型"""
    __tablename__ = 'formal_order'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_no = db.Column(db.String(50), unique=True, nullable=False)
    user_name = db.Column(db.String(50), nullable=False)
    user_phone = db.Column(db.String(20), nullable=False)
    user_address = db.Column(db.Text, nullable=False)
    wheelchair_id = db.Column(db.Integer, db.ForeignKey('wheelchair.id'), nullable=False)
    deposit = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='待配送')
    create_time = db.Column(db.DateTime, default=datetime.utcnow)
    
    wheelchair = db.relationship('Wheelchair', backref='formal_orders')
    
    def to_dict(self):
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
        now = datetime.now()
        timestamp = now.strftime('%Y%m%d%H%M%S')
        random_suffix = str(uuid.uuid4())[:6].upper()
        return f'WR{timestamp}{random_suffix}'

class TempOrder(db.Model):
    """临时预订单模型"""
    __tablename__ = 'temp_order'
    
    id = db.Column(db.String(50), primary_key=True)
    user_name = db.Column(db.String(50))
    user_phone = db.Column(db.String(20))
    user_address = db.Column(db.Text)
    wheelchair_id = db.Column(db.Integer)
    create_time = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __init__(self, user_name, user_phone, user_address, wheelchair_id):
        self.id = str(uuid.uuid4())
        self.user_name = user_name
        self.user_phone = user_phone
        self.user_address = user_address
        self.wheelchair_id = wheelchair_id
        self.create_time = datetime.utcnow()
    
    def get_expire_time(self):
        return self.create_time + timedelta(minutes=30)
    
    def is_expired(self):
        return datetime.utcnow() > self.get_expire_time()

class AdminUser(db.Model):
    """管理用户模型"""
    __tablename__ = 'admin_user'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    is_deleted = db.Column(db.Boolean, default=False)
    
    def set_password(self, password):
        if isinstance(password, str):
            password = password.encode('utf-8')
        salt = bcrypt.gensalt()
        self.password_hash = bcrypt.hashpw(password, salt).decode('utf-8')
    
    def check_password(self, password):
        if isinstance(password, str):
            password = password.encode('utf-8')
        if isinstance(self.password_hash, str):
            password_hash = self.password_hash.encode('utf-8')
        else:
            password_hash = self.password_hash
        return bcrypt.checkpw(password, password_hash)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'role': self.role,
            'is_deleted': self.is_deleted
        }

# 工具函数
def success_response(data=None, message='操作成功'):
    return jsonify({
        'code': 200,
        'message': message,
        'data': data
    })

def error_response(message='操作失败', code=400):
    return jsonify({
        'code': code,
        'message': message
    }), code

def validate_phone(phone):
    import re
    pattern = r'^1[3-9]\d{9}$'
    return re.match(pattern, phone) is not None

# 权限装饰器
def admin_required(f):
    from functools import wraps
    @wraps(f)
    @jwt_required()
    def decorated_function(*args, **kwargs):
        current_user_id = get_jwt_identity()
        user = AdminUser.query.get(int(current_user_id))
        if not user or user.is_deleted:
            return error_response('用户不存在', 401)
        return f(*args, **kwargs)
    return decorated_function

# 客户端API路由
@app.route('/api/wheelchair/search', methods=['GET'])
def search_wheelchairs():
    """轮椅搜索接口"""
    try:
        keyword = request.args.get('keyword', '').strip()
        sort_type = request.args.get('sort_type', '')
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 10))
        
        if page < 1:
            page = 1
        if limit < 1 or limit > 50:
            limit = 10
        
        query = Wheelchair.query.filter(
            Wheelchair.is_deleted == False,
            Wheelchair.is_offline == False
        )
        
        if keyword:
            search_filter = or_(
                Wheelchair.name.contains(keyword),
                Wheelchair.description.contains(keyword),
                Wheelchair.manufacturer.contains(keyword)
            )
            query = query.filter(search_filter)
        
        if sort_type == 'price_asc':
            query = query.order_by(Wheelchair.price.asc())
        elif sort_type == 'price_desc':
            query = query.order_by(Wheelchair.price.desc())
        else:
            query = query.order_by(Wheelchair.id.desc())
        
        total = query.count()
        wheelchairs = query.offset((page - 1) * limit).limit(limit).all()
        
        wheelchair_list = [wheelchair.to_dict() for wheelchair in wheelchairs]
        
        return success_response({
            'list': wheelchair_list,
            'total': total,
            'page': page,
            'limit': limit,
            'pages': (total + limit - 1) // limit
        })
        
    except Exception as e:
        return error_response(f'搜索失败: {str(e)}', 500)

@app.route('/api/wheelchair/detail/<int:wheelchair_id>', methods=['GET'])
def get_wheelchair_detail(wheelchair_id):
    """获取轮椅详情"""
    try:
        wheelchair = Wheelchair.query.filter(
            Wheelchair.id == wheelchair_id,
            Wheelchair.is_deleted == False,
            Wheelchair.is_offline == False
        ).first()
        
        if not wheelchair:
            return error_response('轮椅不存在', 404)
        
        return success_response(wheelchair.to_dict())
        
    except Exception as e:
        return error_response(f'获取轮椅详情失败: {str(e)}', 500)

@app.route('/api/order/precreate', methods=['POST'])
def create_temp_order():
    """创建预订单"""
    try:
        data = request.get_json()
        
        required_fields = ['name', 'phone', 'address', 'wheelchair_id']
        for field in required_fields:
            if field not in data or not data[field]:
                return error_response(f'缺少必需字段: {field}', 400)
        
        user_name = data['name'].strip()
        user_phone = data['phone'].strip()
        user_address = data['address'].strip()
        wheelchair_id = data['wheelchair_id']
        
        if not validate_phone(user_phone):
            return error_response('手机号格式不正确', 400)
        
        wheelchair = Wheelchair.query.filter(
            Wheelchair.id == wheelchair_id,
            Wheelchair.is_deleted == False,
            Wheelchair.is_offline == False,
            Wheelchair.stock > 0
        ).first()
        
        if not wheelchair:
            return error_response('轮椅不存在或库存不足', 404)
        
        temp_order = TempOrder(
            user_name=user_name,
            user_phone=user_phone,
            user_address=user_address,
            wheelchair_id=wheelchair_id
        )
        
        db.session.add(temp_order)
        db.session.commit()
        
        return success_response({
            'pre_order_id': temp_order.id,
            'expire_time': temp_order.get_expire_time().strftime('%Y-%m-%d %H:%M:%S'),
            'wheelchair': wheelchair.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return error_response(f'创建预订单失败: {str(e)}', 500)

@app.route('/api/order/submit', methods=['POST'])
def submit_order():
    """提交正式订单"""
    try:
        data = request.get_json()
        
        if 'pre_order_id' not in data:
            return error_response('缺少预订单ID', 400)
        
        pre_order_id = data['pre_order_id']
        temp_order = TempOrder.query.get(pre_order_id)
        
        if not temp_order:
            return error_response('预订单不存在', 404)
        
        if temp_order.is_expired():
            return error_response('预订单已过期，请重新下单', 400)
        
        wheelchair = Wheelchair.query.filter(
            Wheelchair.id == temp_order.wheelchair_id,
            Wheelchair.is_deleted == False,
            Wheelchair.is_offline == False,
            Wheelchair.stock > 0
        ).first()
        
        if not wheelchair:
            return error_response('轮椅不存在或库存不足', 404)
        
        try:
            formal_order = FormalOrder(
                order_no=FormalOrder.generate_order_no(),
                user_name=temp_order.user_name,
                user_phone=temp_order.user_phone,
                user_address=temp_order.user_address,
                wheelchair_id=temp_order.wheelchair_id,
                deposit=wheelchair.price
            )
            
            wheelchair.reduce_stock(1)
            
            db.session.add(formal_order)
            db.session.delete(temp_order)
            db.session.commit()
            
            return success_response({
                'order_no': formal_order.order_no,
                'order_id': formal_order.id,
                'message': '订单提交成功',
                'order_info': formal_order.to_dict()
            })
            
        except Exception as e:
            db.session.rollback()
            raise e
        
    except Exception as e:
        return error_response(f'提交订单失败: {str(e)}', 500)

# 管理端API路由
@app.route('/api/admin/login', methods=['POST'])
def admin_login():
    """管理员登录"""
    try:
        data = request.get_json()
        
        if 'username' not in data or 'password' not in data:
            return error_response('缺少用户名或密码', 400)
        
        username = data['username']
        password = data['password']
        
        user = AdminUser.query.filter(
            AdminUser.username == username,
            AdminUser.is_deleted == False
        ).first()
        
        if not user or not user.check_password(password):
            return error_response('用户名或密码错误', 401)
        
        access_token = create_access_token(identity=str(user.id))
        
        return success_response({
            'token': access_token,
            'user_info': {
                'id': user.id,
                'username': user.username,
                'role': user.role
            }
        })
        
    except Exception as e:
        return error_response(f'登录失败: {str(e)}', 500)

@app.route('/api/admin/inventory/list', methods=['GET'])
@admin_required
def get_inventory_list():
    """获取库存列表"""
    try:
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 10))
        keyword = request.args.get('keyword', '').strip()
        
        query = Wheelchair.query.filter(Wheelchair.is_deleted == False)
        
        if keyword:
            search_filter = or_(
                Wheelchair.name.contains(keyword),
                Wheelchair.description.contains(keyword),
                Wheelchair.manufacturer.contains(keyword)
            )
            query = query.filter(search_filter)
        
        total = query.count()
        wheelchairs = query.order_by(Wheelchair.id.desc()).offset((page - 1) * limit).limit(limit).all()
        
        wheelchair_list = [wheelchair.to_dict() for wheelchair in wheelchairs]
        
        return success_response({
            'list': wheelchair_list,
            'total': total,
            'page': page,
            'limit': limit
        })
        
    except Exception as e:
        return error_response(f'获取库存列表失败: {str(e)}', 500)

@app.route('/api/admin/inventory/save', methods=['POST'])
@admin_required
def save_wheelchair():
    """新增或修改轮椅"""
    try:
        data = request.get_json()
        
        # 验证必需字段
        required_fields = ['name', 'price']
        for field in required_fields:
            if field not in data or not data[field]:
                return error_response(f'缺少必需字段: {field}', 400)
        
        wheelchair_id = data.get('id')
        name = data['name'].strip()
        price = float(data['price'])
        description = data.get('description', '').strip()
        stock = int(data.get('stock', 1))
        manufacturer = data.get('manufacturer', '').strip()
        
        # 数据验证
        if not name:
            return error_response('轮椅名称不能为空', 400)
        if price <= 0:
            return error_response('价格必须大于0', 400)
        if stock < 0:
            return error_response('库存不能为负数', 400)
        
        if wheelchair_id:
            # 修改轮椅
            wheelchair = Wheelchair.query.get(wheelchair_id)
            if not wheelchair:
                return error_response('轮椅不存在', 404)
            
            wheelchair.name = name
            wheelchair.price = price
            wheelchair.description = description
            wheelchair.stock = stock
            wheelchair.manufacturer = manufacturer
            
            message = '轮椅信息更新成功'
        else:
            # 新增轮椅
            wheelchair = Wheelchair(
                name=name,
                price=price,
                description=description,
                stock=stock,
                manufacturer=manufacturer
            )
            db.session.add(wheelchair)
            
            message = '轮椅添加成功'
        
        db.session.commit()
        
        return success_response({
            'message': message,
            'wheelchair': wheelchair.to_dict()
        })
        
    except ValueError as e:
        return error_response(f'数据格式错误: {str(e)}', 400)
    except Exception as e:
        db.session.rollback()
        return error_response(f'保存轮椅失败: {str(e)}', 500)

@app.route('/api/admin/inventory/operate', methods=['POST'])
@admin_required
def operate_wheelchair():
    """操作轮椅（删除/下架/上架/批量状态更新）"""
    try:
        data = request.get_json()
        
        # 支持不同的操作类型
        action = data.get('action')
        operate_type = data.get('operate_type')
        
        # 兼容新旧API格式
        if action:
            operate_type = action
        
        # 处理批量状态更新
        if operate_type == 'batch_status':
            ids = data.get('ids', [])
            status = data.get('status')
            
            if not ids or not status:
                return error_response('批量操作需要提供ids和status', 400)
            
            updated_count = 0
            
            for wheelchair_id in ids:
                wheelchair = Wheelchair.query.get(wheelchair_id)
                if wheelchair:
                    wheelchair.status = status
                    updated_count += 1
            
            db.session.commit()
            
            return success_response({
                'message': f'成功更新 {updated_count} 个轮椅状态',
                'updated_count': updated_count
            })
        
        # 单个轮椅操作
        wheelchair_id = data.get('id')
        if not wheelchair_id or not operate_type:
            return error_response('缺少必需字段: id 和 operate_type/action', 400)
        
        # 获取轮椅
        wheelchair = Wheelchair.query.get(wheelchair_id)
        if not wheelchair:
            return error_response('轮椅不存在', 404)
        
        # 执行操作
        if operate_type == 'delete':
            wheelchair.is_deleted = True
            message = '轮椅删除成功'
        elif operate_type == 'offline':
            wheelchair.is_offline = True
            message = '轮椅下架成功'
        elif operate_type == 'online':
            wheelchair.is_offline = False
            message = '轮椅上架成功'
        else:
            return error_response('无效的操作类型', 400)
        
        db.session.commit()
        
        return success_response({
            'message': message,
            'wheelchair': wheelchair.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return error_response(f'操作失败: {str(e)}', 500)

@app.route('/api/admin/order/list', methods=['GET'])
@admin_required
def get_order_list():
    """获取订单列表"""
    try:
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 10))
        status = request.args.get('status', '').strip()
        
        query = FormalOrder.query
        
        if status:
            query = query.filter(FormalOrder.status == status)
        
        total = query.count()
        orders = query.order_by(FormalOrder.create_time.desc()).offset((page - 1) * limit).limit(limit).all()
        
        order_list = [order.to_dict() for order in orders]
        
        return success_response({
            'list': order_list,
            'total': total,
            'page': page,
            'limit': limit
        })
        
    except Exception as e:
        return error_response(f'获取订单列表失败: {str(e)}', 500)

# 健康检查接口
@app.route('/health')
def health_check():
    return success_response({
        'service': '在线轮椅租赁系统',
        'version': '1.0.0',
        'status': 'healthy'
    })

# 根路径
@app.route('/')
def index():
    return success_response({
        'service': '在线轮椅租赁系统',
        'version': '1.0.0',
        'endpoints': {
            'client_api': '/api',
            'admin_api': '/api/admin',
            'health': '/health'
        }
    })

# 初始化数据库
def init_database():
    """初始化数据库表结构和基础数据"""
    with app.app_context():
        db.create_all()
        print("数据库表创建完成")
        
        # 检查是否需要初始化数据
        if AdminUser.query.count() == 0:
            # 创建默认管理员
            admin = AdminUser(
                username='admin',
                role='admin'
            )
            admin.set_password('123456')
            
            operator = AdminUser(
                username='operator1',
                role='operator'
            )
            operator.set_password('123456')
            
            db.session.add(admin)
            db.session.add(operator)
            
            # 创建示例轮椅数据
            wheelchairs = [
                Wheelchair(
                    name='电动轮椅豪华版',
                    description='配备GPS定位、智能刹车系统的高端电动轮椅',
                    price=200.0,
                    stock=3,
                    manufacturer='智能康复设备有限公司'
                ),
                Wheelchair(
                    name='手动轮椅标准版',
                    description='轻便耐用的手动轮椅，适合日常使用',
                    price=80.0,
                    stock=5,
                    manufacturer='康复器械制造厂'
                ),
                Wheelchair(
                    name='电动轮椅经济版',
                    description='性价比高的电动轮椅，操作简单',
                    price=120.0,
                    stock=4,
                    manufacturer='医疗设备公司'
                ),
                Wheelchair(
                    name='折叠轮椅便携版',
                    description='可折叠设计，方便携带和存储',
                    price=100.0,
                    stock=6,
                    manufacturer='便民医疗器械'
                )
            ]
            
            for wheelchair in wheelchairs:
                db.session.add(wheelchair)
            
            db.session.commit()
            print("基础数据初始化完成")
            print("默认管理员账号: admin / 123456")
            print("默认操作员账号: operator1 / 123456")

if __name__ == '__main__':
    # 初始化数据库
    init_database()
    
    # 启动应用
    print("正在启动在线轮椅租赁系统后端服务...")
    print("客户端API: http://localhost:5001/api")
    print("管理端API: http://localhost:5001/api/admin")
    print("健康检查: http://localhost:5001/health")
    
    app.run(
        host='0.0.0.0',
        port=5001,
        debug=True
    )