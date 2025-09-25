#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
客户端API路由
处理面向普通用户的API请求
"""

import re
from flask import Blueprint, request, jsonify
from models.wheelchair import Wheelchair
from models.order import TempOrder, FormalOrder
from utils.validators import validate_phone, validate_required_fields
from utils.response import success_response, error_response

# 创建蓝图
client_bp = Blueprint('client_api', __name__)

@client_bp.route('/wheelchair/search', methods=['GET'])
def search_wheelchairs():
    """轮椅搜索接口"""
    try:
        # 获取查询参数
        keyword = request.args.get('keyword', '').strip()
        sort_type = request.args.get('sort_type', '')
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 10))
        
        # 参数验证
        if page < 1:
            page = 1
        if limit < 1 or limit > 50:
            limit = 10
        
        # 搜索轮椅
        wheelchairs, total = Wheelchair.search(
            keyword=keyword if keyword else None,
            sort_type=sort_type if sort_type else None,
            page=page,
            limit=limit,
            include_offline=False
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
        return error_response(f'搜索失败: {str(e)}', 500)

@client_bp.route('/wheelchair/detail/<int:wheelchair_id>', methods=['GET'])
def get_wheelchair_detail(wheelchair_id):
    """获取轮椅详情"""
    try:
        wheelchair = Wheelchair.get_by_id(wheelchair_id)
        
        if not wheelchair:
            return error_response('轮椅不存在', 404)
        
        if wheelchair.is_deleted or wheelchair.is_offline:
            return error_response('轮椅已下架', 404)
        
        return success_response(wheelchair.to_dict())
        
    except Exception as e:
        return error_response(f'获取轮椅详情失败: {str(e)}', 500)

@client_bp.route('/order/precreate', methods=['POST'])
def create_temp_order():
    """创建预订单"""
    try:
        data = request.get_json()
        
        # 验证必需字段
        required_fields = ['name', 'phone', 'address', 'wheelchair_id']
        missing_fields = validate_required_fields(data, required_fields)
        if missing_fields:
            return error_response(f'缺少必需字段: {", ".join(missing_fields)}', 400)
        
        # 获取数据
        user_name = data['name'].strip()
        user_phone = data['phone'].strip()
        user_address = data['address'].strip()
        wheelchair_id = data['wheelchair_id']
        
        # 验证数据
        if not user_name:
            return error_response('用户姓名不能为空', 400)
        
        if not validate_phone(user_phone):
            return error_response('手机号格式不正确', 400)
        
        if not user_address:
            return error_response('收货地址不能为空', 400)
        
        # 验证轮椅是否可用
        wheelchair = Wheelchair.get_available_by_id(wheelchair_id)
        if not wheelchair:
            return error_response('轮椅不存在或已下架', 404)
        
        if wheelchair.stock <= 0:
            return error_response('轮椅库存不足', 400)
        
        # 创建临时订单
        temp_order = TempOrder(
            user_name=user_name,
            user_phone=user_phone,
            user_address=user_address,
            wheelchair_id=wheelchair_id
        )
        
        from app import db
        db.session.add(temp_order)
        db.session.commit()
        
        return success_response({
            'pre_order_id': temp_order.id,
            'expire_time': temp_order.get_expire_time().strftime('%Y-%m-%d %H:%M:%S'),
            'wheelchair': wheelchair.to_dict()
        })
        
    except Exception as e:
        from app import db
        db.session.rollback()
        return error_response(f'创建预订单失败: {str(e)}', 500)

@client_bp.route('/order/submit', methods=['POST'])
def submit_order():
    """提交正式订单（模拟支付）"""
    try:
        data = request.get_json()
        
        # 验证必需字段
        if 'pre_order_id' not in data:
            return error_response('缺少预订单ID', 400)
        
        pre_order_id = data['pre_order_id']
        
        # 获取临时订单
        temp_order = TempOrder.get_by_id(pre_order_id)
        if not temp_order:
            return error_response('预订单不存在', 404)
        
        # 检查是否过期
        if temp_order.is_expired():
            return error_response('预订单已过期，请重新下单', 400)
        
        # 验证轮椅是否仍然可用
        wheelchair = Wheelchair.get_available_by_id(temp_order.wheelchair_id)
        if not wheelchair:
            return error_response('轮椅不存在或已下架', 404)
        
        if wheelchair.stock <= 0:
            return error_response('轮椅库存不足', 400)
        
        # 开始事务处理
        from app import db
        
        try:
            # 创建正式订单
            formal_order = FormalOrder(
                user_name=temp_order.user_name,
                user_phone=temp_order.user_phone,
                user_address=temp_order.user_address,
                wheelchair_id=temp_order.wheelchair_id,
                deposit=wheelchair.price  # 定金等于租赁价格
            )
            
            # 减少库存
            wheelchair.reduce_stock(1)
            
            # 保存正式订单
            db.session.add(formal_order)
            
            # 删除临时订单
            db.session.delete(temp_order)
            
            # 提交事务
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

@client_bp.route('/order/detail/<order_no>', methods=['GET'])
def get_order_detail(order_no):
    """获取订单详情（通过订单号）"""
    try:
        order = FormalOrder.query.filter_by(order_no=order_no).first()
        
        if not order:
            return error_response('订单不存在', 404)
        
        return success_response(order.to_dict())
        
    except Exception as e:
        return error_response(f'获取订单详情失败: {str(e)}', 500)