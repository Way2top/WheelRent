# 在线轮椅租赁系统

一个为失能老人提供智能轮椅租赁服务的综合平台，采用前后端分离架构，包含面向顾客的客户端和面向内部员工的管理端。

## 📋 项目概述

本系统主要解决失能老人轮椅租赁需求，为用户提供便捷的在线租赁服务，为企业提供高效的库存和订单管理工具。系统具有适老化设计特色，支持大字模式，操作简便，界面友好。

## ✨ 功能特色

### 🎯 核心功能
- **轮椅搜索租赁**：支持关键词搜索、价格排序、详情查看
- **在线下单**：预订单+正式订单双重保障，支持模拟支付
- **库存管理**：实时库存更新、轮椅增删改查、操作日志
- **订单管理**：订单状态跟踪、库存自动同步
- **用户权限**：管理员、操作员分级权限控制
- **适老化设计**：大字模式切换，适合老年用户操作

### 🔐 用户角色
- **普通用户**：无需注册，直接浏览和租赁轮椅
- **操作员**：管理库存、处理订单、查看操作日志
- **管理员**：全部权限，包括用户管理、系统配置

## 🛠 技术栈

### 后端技术
- **框架**：Flask 2.0+
- **数据库**：SQLite 3.30+
- **ORM**：Flask-SQLAlchemy
- **认证**：Flask-JWT-Extended
- **跨域**：Flask-CORS
- **密码加密**：bcrypt

### 前端技术
- **框架**：Vue 3 (Composition API)
- **UI库**：Element Plus
- **状态管理**：Pinia
- **路由**：Vue Router
- **HTTP客户端**：Axios
- **打包工具**：Vite

## 📁 项目结构

```
WheelRent/
├── .trae/
│   └── documents/          # 产品需求文档和技术架构文档
├── backend/                # Flask后端应用
│   ├── models/             # 数据模型
│   ├── routes/             # API路由
│   ├── utils/              # 工具函数
│   ├── app_simple.py       # 主应用文件
│   ├── requirements.txt    # Python依赖
│   └── wheelchair_rental.db # SQLite数据库
├── frontend/
│   ├── client/             # Vue客户端应用
│   └── admin/              # Vue管理端应用
├── database/
│   └── init_sqlite.sql     # 数据库初始化脚本
└── README.md               # 项目说明文档
```

## 🚀 环境要求

- **Python**: 3.8+
- **Node.js**: 16+
- **npm**: 8+

## 📦 安装与启动

### 1. 克隆项目
```bash
git clone <repository-url>
cd WheelRent
```

### 2. 后端启动
```bash
# 进入后端目录
cd backend

# 创建虚拟环境（如果没有）
python -m venv venv

# 激活虚拟环境
source venv/bin/activate  # macOS/Linux
# 或
venv\Scripts\activate     # Windows

# 安装依赖
pip install -r requirements.txt

# 启动后端服务
python app_simple.py
```

### 3. 客户端启动
```bash
# 新开终端，进入客户端目录
cd frontend/client

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

### 4. 管理端启动
```bash
# 新开终端，进入管理端目录
cd frontend/admin

# 安装依赖
npm install

# 启动开发服务器（指定端口避免冲突）
npm run dev -- --port 5174
```

## 🌐 访问地址

启动成功后，您可以通过以下地址访问系统：

### 👥 客户端界面（普通用户）
**🔗 http://localhost:5173/**
- 轮椅搜索和浏览
- 轮椅详情查看
- 在线租赁下单
- 支付流程
- 大字模式切换

### 🔐 管理端界面（管理员）
**🔗 http://localhost:5174/**
- 管理员登录
- 库存管理
- 订单管理
- 用户管理
- 操作日志查看

### 🔧 后端API
**🔗 http://localhost:5001/**
- 客户端API：`/api/*`
- 管理端API：`/api/admin/*`
- 健康检查：`/health`

## 🔑 默认账号信息

### 管理员账号
- **用户名**：`admin`
- **密码**：`123456`
- **权限**：全部权限

### 操作员账号
- **用户名**：`operator1`
- **密码**：`123456`
- **权限**：库存管理、订单管理

## 📚 API接口说明

### 客户端API
- `GET /api/wheelchair/search` - 轮椅搜索
- `GET /api/wheelchair/detail/<id>` - 轮椅详情
- `POST /api/order/precreate` - 创建预订单
- `POST /api/order/submit` - 提交正式订单

### 管理端API（需JWT认证）
- `POST /api/admin/login` - 管理员登录
- `GET /api/admin/inventory/list` - 库存列表
- `POST /api/admin/inventory/save` - 保存库存
- `GET /api/admin/order/list` - 订单列表
- `POST /api/admin/order/update/status` - 更新订单状态
- `GET /api/admin/user/list` - 用户列表（仅管理员）

## 🎯 使用指南

### 普通用户操作流程
1. 访问客户端界面：http://localhost:5173
2. 搜索或浏览轮椅产品
3. 查看轮椅详情
4. 填写租赁信息创建订单
5. 确认支付完成租赁

### 管理员操作流程
1. 访问管理端界面：http://localhost:5174
2. 使用管理员账号登录
3. 管理轮椅库存
4. 处理用户订单
5. 查看操作日志

## ⚠️ 注意事项

### 启动顺序
1. **先启动后端服务**（Flask）
2. **再启动前端应用**（Vue客户端和管理端）

### 端口说明
- **后端服务**：5001端口
- **客户端**：5173端口
- **管理端**：5174端口

### 数据库
- 使用SQLite文件数据库，位于`backend/wheelchair_rental.db`
- 首次启动会自动创建数据库表和初始数据
- 包含4种轮椅产品和2个管理员账号

### 开发环境
- 确保Python虚拟环境已激活
- 确保Node.js版本兼容
- 如遇端口冲突，可修改配置文件中的端口设置

## 🔧 常见问题

### Q: 后端启动失败？
A: 检查Python虚拟环境是否激活，依赖是否安装完整

### Q: 前端无法访问后端API？
A: 确认后端服务已启动，检查CORS配置

### Q: 管理端登录失败？
A: 确认使用正确的用户名密码，检查JWT配置

### Q: 数据库连接错误？
A: 确认SQLite数据库文件存在，检查文件权限

## 🎨 项目特色

- **适老化设计**：大字模式、简化操作、清晰界面
- **前后端分离**：标准RESTful API架构
- **权限分级**：管理员、操作员两级权限管理
- **事务安全**：订单创建采用预订单+正式订单模式
- **操作审计**：完整的管理操作日志记录
- **响应式设计**：支持桌面端和移动端访问

## 📄 许可证

本项目仅用于学习和研究目的。

---

**开发完成时间**：2025年
**技术支持**：Vue 3 + Flask + SQLite
**适用场景**：轮椅租赁、医疗器械管理、适老化服务平台