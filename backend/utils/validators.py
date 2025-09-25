#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据验证工具函数
"""

import re

def validate_phone(phone):
    """验证手机号格式
    
    Args:
        phone: 手机号字符串
    
    Returns:
        bool: 是否为有效的手机号
    """
    if not phone:
        return False
    
    # 中国大陆手机号正则表达式
    pattern = r'^1[3-9]\d{9}$'
    return bool(re.match(pattern, phone))

def validate_email(email):
    """验证邮箱格式
    
    Args:
        email: 邮箱字符串
    
    Returns:
        bool: 是否为有效的邮箱
    """
    if not email:
        return False
    
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_required_fields(data, required_fields):
    """验证必需字段
    
    Args:
        data: 数据字典
        required_fields: 必需字段列表
    
    Returns:
        list: 缺少的字段列表
    """
    if not isinstance(data, dict):
        return required_fields
    
    missing_fields = []
    for field in required_fields:
        if field not in data or data[field] is None:
            missing_fields.append(field)
        elif isinstance(data[field], str) and not data[field].strip():
            missing_fields.append(field)
    
    return missing_fields

def validate_password_strength(password):
    """验证密码强度
    
    Args:
        password: 密码字符串
    
    Returns:
        tuple: (是否有效, 错误消息)
    """
    if not password:
        return False, '密码不能为空'
    
    if len(password) < 6:
        return False, '密码长度至少6位'
    
    if len(password) > 50:
        return False, '密码长度不能超过50位'
    
    # 可以添加更多密码强度验证规则
    # 例如：必须包含数字、字母、特殊字符等
    
    return True, '密码格式正确'

def validate_price(price):
    """验证价格格式
    
    Args:
        price: 价格值
    
    Returns:
        tuple: (是否有效, 错误消息)
    """
    try:
        price_float = float(price)
        if price_float < 0:
            return False, '价格不能为负数'
        if price_float > 999999:
            return False, '价格不能超过999999'
        return True, '价格格式正确'
    except (ValueError, TypeError):
        return False, '价格格式不正确'

def validate_stock(stock):
    """验证库存数量
    
    Args:
        stock: 库存数量
    
    Returns:
        tuple: (是否有效, 错误消息)
    """
    try:
        stock_int = int(stock)
        if stock_int < 0:
            return False, '库存不能为负数'
        if stock_int > 99999:
            return False, '库存不能超过99999'
        return True, '库存格式正确'
    except (ValueError, TypeError):
        return False, '库存格式不正确'

def sanitize_string(text, max_length=None):
    """清理字符串
    
    Args:
        text: 输入字符串
        max_length: 最大长度限制
    
    Returns:
        str: 清理后的字符串
    """
    if not isinstance(text, str):
        return ''
    
    # 去除首尾空白
    text = text.strip()
    
    # 长度限制
    if max_length and len(text) > max_length:
        text = text[:max_length]
    
    return text

def validate_pagination(page, limit, max_limit=100):
    """验证分页参数
    
    Args:
        page: 页码
        limit: 每页数量
        max_limit: 最大每页数量
    
    Returns:
        tuple: (页码, 每页数量)
    """
    try:
        page = int(page) if page else 1
        limit = int(limit) if limit else 10
    except (ValueError, TypeError):
        page = 1
        limit = 10
    
    # 确保页码至少为1
    if page < 1:
        page = 1
    
    # 确保每页数量在合理范围内
    if limit < 1:
        limit = 10
    elif limit > max_limit:
        limit = max_limit
    
    return page, limit