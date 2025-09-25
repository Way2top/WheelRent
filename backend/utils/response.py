#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API响应工具函数
统一API响应格式
"""

from flask import jsonify

def success_response(data=None, message='操作成功', code=200):
    """成功响应
    
    Args:
        data: 响应数据
        message: 响应消息
        code: 状态码
    
    Returns:
        Response: Flask响应对象
    """
    response_data = {
        'code': code,
        'message': message
    }
    
    if data is not None:
        response_data['data'] = data
    
    return jsonify(response_data), code

def error_response(message='操作失败', code=400, error_code=None):
    """错误响应
    
    Args:
        message: 错误消息
        code: HTTP状态码
        error_code: 业务错误码
    
    Returns:
        Response: Flask响应对象
    """
    response_data = {
        'code': code,
        'message': message
    }
    
    if error_code:
        response_data['error_code'] = error_code
    
    return jsonify(response_data), code

def paginated_response(items, total, page, limit, message='获取成功'):
    """分页响应
    
    Args:
        items: 数据列表
        total: 总数量
        page: 当前页码
        limit: 每页数量
        message: 响应消息
    
    Returns:
        Response: Flask响应对象
    """
    pages = (total + limit - 1) // limit if total > 0 else 0
    
    data = {
        'list': items,
        'pagination': {
            'total': total,
            'page': page,
            'limit': limit,
            'pages': pages,
            'has_next': page < pages,
            'has_prev': page > 1
        }
    }
    
    return success_response(data, message)

def validation_error_response(errors):
    """验证错误响应
    
    Args:
        errors: 错误信息字典或列表
    
    Returns:
        Response: Flask响应对象
    """
    if isinstance(errors, dict):
        message = '数据验证失败'
        return jsonify({
            'code': 400,
            'message': message,
            'errors': errors
        }), 400
    elif isinstance(errors, list):
        message = '; '.join(errors)
        return error_response(message, 400)
    else:
        return error_response(str(errors), 400)

def not_found_response(resource='资源'):
    """404响应
    
    Args:
        resource: 资源名称
    
    Returns:
        Response: Flask响应对象
    """
    return error_response(f'{resource}不存在', 404)

def unauthorized_response(message='未授权访问'):
    """401响应
    
    Args:
        message: 错误消息
    
    Returns:
        Response: Flask响应对象
    """
    return error_response(message, 401)

def forbidden_response(message='权限不足'):
    """403响应
    
    Args:
        message: 错误消息
    
    Returns:
        Response: Flask响应对象
    """
    return error_response(message, 403)

def server_error_response(message='服务器内部错误'):
    """500响应
    
    Args:
        message: 错误消息
    
    Returns:
        Response: Flask响应对象
    """
    return error_response(message, 500)

def created_response(data=None, message='创建成功'):
    """201响应
    
    Args:
        data: 响应数据
        message: 响应消息
    
    Returns:
        Response: Flask响应对象
    """
    return success_response(data, message, 201)

def no_content_response():
    """204响应
    
    Returns:
        Response: Flask响应对象
    """
    return '', 204