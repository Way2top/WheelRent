#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
管理端API路由
处理面向管理员和操作员的API请求
"""

from functools import wraps
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from models.user import AdminUser
from models.wheelchair import Wheelchair
from models.order import FormalOrder
from models.log import OperationLog
from utils.validators import validate_required_fields
from utils.response import success_response, error_response

# 创建蓝图
admin_bp = Blueprint('admin_api', __name__)

# 权限装饰器
def admin_required(f):
    """管理员权限装饰器"""
    @wraps(f)
    @jwt_required()
    def decorated_function(*args, **kwargs):
        current_user_id = get_jwt_identity()
        user = AdminUser.get_by_id(current_user_id)
        
        if not user or not user.is_admin():
            return error_response('需要管理员权限', 403)
        
        return f(*args, **kwargs)
    return decorated_function

def operator_required(f):
    """操作员权限装饰器（管理员和操作员都可以）"""
    @wraps(f)
    @jwt_required()
    def decorated_function(*args, **kwargs):
        current_user_id = get_jwt_identity()
        user = AdminUser.get_by_id(current_user_id)
        
        if not user or not (user.is_admin() or user.is_operator()):
            return error_response('需要操作员权限', 403)
        
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/login', methods=['POST'])
def admin_login():
    """管理员登录"""
    try:
        data = request.get_json()
        
        # 验证必需字段
        required_fields = ['username', 'password']
        missing_fields = validate_required_fields(data, required_fields)
        if missing_fields:
            return error_response(f'缺少必需字段: {", ".join(missing_fields)}', 400)
        
        username = data['username'].strip()
        password = data['password']
        
        # 用户认证
        user, message = AdminUser.authenticate(username, password)
        
        if not user:
            # 记录登录失败日志
            return error_response(message, 401)
        
        # 生成JWT令牌
        access_token = create_access_token(identity=user.id)
        
        # 记录登录成功日志
        OperationLog.log_operation(user.id, OperationLog.TYPE_LOGIN)
        
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

@admin_bp.route('/logout', methods=['POST'])
@jwt_required()
def admin_logout():
    """管理员登出"""
    try:
        current_user_id = get_jwt_identity()
        
        # 记录登出日志
        OperationLog.log_operation(current_user_id, OperationLog.TYPE_LOGOUT)
        
        return success_response({'message': '登出成功'})
        
    except Exception as e:
        return error_response(f'登出失败: {str(e)}', 500)

@admin_bp.route('/inventory/list', methods=['GET'])
@operator_required
def get_inventory_list():
    """获取库存列表"""
    try:
        # 获取查询参数
        keyword = request.args.get('keyword', '').strip()
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 10))
        include_offline = request.args.get('include_offline', 'false').lower() == 'true'
        
        # 参数验证
        if page < 1:
            page = 1
        if limit < 1 or limit > 50:
            limit = 10
        
        # 搜索轮椅
        wheelchairs, total = Wheelchair.search(
            keyword=keyword if keyword else None,
            page=page,
            limit=limit,
            include_offline=include_offline
        )
        
        # 转换为字典格式
        wheelchair_list = [wheelchair.to_dict() for wheelchair in wheelchairs]
        
        return success_response({
            'list': wheelchair_list,
            'total': total,
            'page': page,
            'limit': limit,
            'pages': (total + limit - 1) // limit
        })
        
    except ValueError as e:
        return error_response(f'参数错误: {str(e)}', 400)
    except Exception as e:
        return error_response(f'获取库存列表失败: {str(e)}', 500)

@admin_bp.route('/inventory/save', methods=['POST'])
@operator_required
def save_wheelchair():
    """新增或修改轮椅"""
    try:
        data = request.get_json()
        current_user_id = get_jwt_identity()
        
        # 验证必需字段
        required_fields = ['name', 'price']
        missing_fields = validate_required_fields(data, required_fields)
        if missing_fields:
            return error_response(f'缺少必需字段: {", ".join(missing_fields)}', 400)
        
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
        
        from app import db
        
        if wheelchair_id:
            # 修改轮椅
            wheelchair = Wheelchair.get_by_id(wheelchair_id, include_deleted=True)
            if not wheelchair:
                return error_response('轮椅不存在', 404)
            
            wheelchair.name = name
            wheelchair.price = price
            wheelchair.description = description
            wheelchair.stock = stock
            wheelchair.manufacturer = manufacturer
            
            operation_type = OperationLog.TYPE_UPDATE_WHEELCHAIR
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
            
            operation_type = OperationLog.TYPE_ADD_WHEELCHAIR
            message = '轮椅添加成功'
        
        db.session.commit()
        
        # 记录操作日志
        OperationLog.log_operation(current_user_id, operation_type, wheelchair.id)
        
        return success_response({
            'message': message,
            'wheelchair': wheelchair.to_dict()
        })
        
    except ValueError as e:
        return error_response(f'数据格式错误: {str(e)}', 400)
    except Exception as e:
        from app import db
        db.session.rollback()
        return error_response(f'保存轮椅失败: {str(e)}', 500)

@admin_bp.route('/inventory/operate', methods=['POST'])
@operator_required
def operate_wheelchair():
    """操作轮椅（删除/下架/上架）"""
    try:
        data = request.get_json()
        current_user_id = get_jwt_identity()
        
        # 验证必需字段
        required_fields = ['id', 'operate_type']
        missing_fields = validate_required_fields(data, required_fields)
        if missing_fields:
            return error_response(f'缺少必需字段: {", ".join(missing_fields)}', 400)
        
        wheelchair_id = data['id']
        operate_type = data['operate_type']
        
        # 获取轮椅
        wheelchair = Wheelchair.get_by_id(wheelchair_id, include_deleted=True)
        if not wheelchair:
            return error_response('轮椅不存在', 404)
        
        from app import db
        
        # 执行操作
        if operate_type == 'delete':
            wheelchair.soft_delete()
            log_type = OperationLog.TYPE_DELETE_WHEELCHAIR
            message = '轮椅删除成功'
        elif operate_type == 'offline':
            wheelchair.set_offline()
            log_type = OperationLog.TYPE_OFFLINE_WHEELCHAIR
            message = '轮椅下架成功'
        elif operate_type == 'online':
            wheelchair.set_online()
            log_type = OperationLog.TYPE_ONLINE_WHEELCHAIR
            message = '轮椅上架成功'
        else:
            return error_response('无效的操作类型', 400)
        
        db.session.commit()
        
        # 记录操作日志
        OperationLog.log_operation(current_user_id, log_type, wheelchair.id)
        
        return success_response({
            'message': message,
            'wheelchair': wheelchair.to_dict()
        })
        
    except Exception as e:
        from app import db
        db.session.rollback()
        return error_response(f'操作失败: {str(e)}', 500)

@admin_bp.route('/order/list', methods=['GET'])
@operator_required
def get_order_list():
    """获取订单列表"""
    try:
        # 获取查询参数
        status = request.args.get('status', '').strip()
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 10))
        
        # 参数验证
        if page < 1:
            page = 1
        if limit < 1 or limit > 50:
            limit = 10
        
        # 获取订单列表
        orders, total = FormalOrder.get_all(
            page=page,
            limit=limit,
            status_filter=status if status else None
        )
        
        # 转换为字典格式
        order_list = [order.to_dict() for order in orders]
        
        return success_response({
            'list': order_list,
            'total': total,
            'page': page,
            'limit': limit,
            'pages': (total + limit - 1) // limit
        })
        
    except ValueError as e:
        return error_response(f'参数错误: {str(e)}', 400)
    except Exception as e:
        return error_response(f'获取订单列表失败: {str(e)}', 500)

@admin_bp.route('/order/update/status', methods=['POST'])
@operator_required
def update_order_status():
    """更新订单状态"""
    try:
        data = request.get_json()
        current_user_id = get_jwt_identity()
        
        # 验证必需字段
        required_fields = ['order_id', 'new_status']
        missing_fields = validate_required_fields(data, required_fields)
        if missing_fields:
            return error_response(f'缺少必需字段: {", ".join(missing_fields)}', 400)
        
        order_id = data['order_id']
        new_status = data['new_status']
        
        # 获取订单
        order = FormalOrder.query.get(order_id)
        if not order:
            return error_response('订单不存在', 404)
        
        # 更新状态
        success, message = order.update_status(new_status)
        if not success:
            return error_response(message, 400)
        
        from app import db
        
        # 如果订单被取消，需要恢复库存
        if new_status == FormalOrder.STATUS_CANCELLED:
            wheelchair = Wheelchair.get_by_id(order.wheelchair_id)
            if wheelchair:
                wheelchair.increase_stock(1)
        
        db.session.commit()
        
        # 记录操作日志
        OperationLog.log_operation(current_user_id, OperationLog.TYPE_UPDATE_ORDER_STATUS, order.id)
        
        return success_response({
            'message': message,
            'order': order.to_dict()
        })
        
    except Exception as e:
        from app import db
        db.session.rollback()
        return error_response(f'更新订单状态失败: {str(e)}', 500)

@admin_bp.route('/user/list', methods=['GET'])
@admin_required
def get_user_list():
    """获取用户列表（仅管理员）"""
    try:
        # 获取查询参数
        role = request.args.get('role', '').strip()
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 10))
        
        # 参数验证
        if page < 1:
            page = 1
        if limit < 1 or limit > 50:
            limit = 10
        
        # 获取用户列表
        users, total = AdminUser.get_all(
            page=page,
            limit=limit,
            role_filter=role if role else None
        )
        
        # 转换为字典格式
        user_list = [user.to_dict() for user in users]
        
        return success_response({
            'list': user_list,
            'total': total,
            'page': page,
            'limit': limit,
            'pages': (total + limit - 1) // limit
        })
        
    except ValueError as e:
        return error_response(f'参数错误: {str(e)}', 400)
    except Exception as e:
        return error_response(f'获取用户列表失败: {str(e)}', 500)

@admin_bp.route('/user/save', methods=['POST'])
@admin_required
def save_user():
    """新增或修改用户（仅管理员）"""
    try:
        data = request.get_json()
        current_user_id = get_jwt_identity()
        
        # 验证必需字段
        required_fields = ['username', 'role']
        missing_fields = validate_required_fields(data, required_fields)
        if missing_fields:
            return error_response(f'缺少必需字段: {", ".join(missing_fields)}', 400)
        
        user_id = data.get('id')
        username = data['username'].strip()
        role = data['role']
        password = data.get('password', '').strip()
        
        # 数据验证
        if not username:
            return error_response('用户名不能为空', 400)
        
        if role not in AdminUser.VALID_ROLES:
            return error_response('无效的角色', 400)
        
        from app import db
        
        if user_id:
            # 修改用户
            user = AdminUser.get_by_id(user_id)
            if not user:
                return error_response('用户不存在', 404)
            
            # 检查用户名是否重复
            if AdminUser.username_exists(username, exclude_id=user_id):
                return error_response('用户名已存在', 400)
            
            user.username = username
            user.role = role
            
            # 如果提供了新密码，则更新密码
            if password:
                user.set_password(password)
            
            operation_type = OperationLog.TYPE_UPDATE_USER
            message = '用户信息更新成功'
        else:
            # 新增用户
            if not password:
                return error_response('新增用户时密码不能为空', 400)
            
            # 检查用户名是否重复
            if AdminUser.username_exists(username):
                return error_response('用户名已存在', 400)
            
            user = AdminUser(username=username, password=password, role=role)
            db.session.add(user)
            
            operation_type = OperationLog.TYPE_ADD_USER
            message = '用户添加成功'
        
        db.session.commit()
        
        # 记录操作日志
        OperationLog.log_operation(current_user_id, operation_type, user.id)
        
        return success_response({
            'message': message,
            'user': user.to_dict()
        })
        
    except Exception as e:
        from app import db
        db.session.rollback()
        return error_response(f'保存用户失败: {str(e)}', 500)