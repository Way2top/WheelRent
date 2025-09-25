#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
路由包初始化文件
"""

# 导入所有路由蓝图
from .client_api import client_bp
from .admin_api import admin_bp

__all__ = ['client_bp', 'admin_