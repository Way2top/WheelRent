-- 在线轮椅租赁系统数据库初始化脚本
-- SQLite 3.30+

-- 删除已存在的表（如果存在）
DROP TABLE IF EXISTS operation_log;
DROP TABLE IF EXISTS temp_order;
DROP TABLE IF EXISTS formal_order;
DROP TABLE IF EXISTS admin_user;
DROP TABLE IF EXISTS wheelchair;

-- 创建轮椅表
CREATE TABLE wheelchair (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    price REAL NOT NULL,
    stock INTEGER NOT NULL DEFAULT 1,
    manufacturer VARCHAR(100),
    is_offline BOOLEAN DEFAULT 0,
    is_deleted BOOLEAN DEFAULT 0
);

-- 创建轮椅表索引
CREATE INDEX idx_wheelchair_name ON wheelchair(name);
CREATE INDEX idx_wheelchair_price ON wheelchair(price);
CREATE INDEX idx_wheelchair_stock ON wheelchair(stock);

-- 创建正式订单表
CREATE TABLE formal_order (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_no VARCHAR(50) UNIQUE NOT NULL,
    user_name VARCHAR(50) NOT NULL,
    user_phone VARCHAR(20) NOT NULL,
    user_address TEXT NOT NULL,
    wheelchair_id INTEGER NOT NULL,
    deposit REAL NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT '待配送',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (wheelchair_id) REFERENCES wheelchair(id)
);

-- 创建正式订单表索引
CREATE INDEX idx_formal_order_no ON formal_order(order_no);
CREATE INDEX idx_formal_order_status ON formal_order(status);
CREATE INDEX idx_formal_order_create_time ON formal_order(create_time DESC);

-- 创建管理用户表
CREATE TABLE admin_user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL CHECK (role IN ('operator', 'admin')),
    is_deleted BOOLEAN DEFAULT 0
);

-- 创建管理用户表索引
CREATE INDEX idx_admin_user_username ON admin_user(username);
CREATE INDEX idx_admin_user_role ON admin_user(role);

-- 创建操作日志表
CREATE TABLE operation_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    operator_id INTEGER NOT NULL,
    operate_type VARCHAR(50) NOT NULL,
    target_id INTEGER,
    operate_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (operator_id) REFERENCES admin_user(id)
);

-- 创建操作日志表索引
CREATE INDEX idx_operation_log_operator ON operation_log(operator_id);
CREATE INDEX idx_operation_log_time ON operation_log(operate_time DESC);
CREATE INDEX idx_operation_log_type ON operation_log(operate_type);

-- 创建临时预订单表
CREATE TABLE temp_order (
    id VARCHAR(50) PRIMARY KEY,
    user_name VARCHAR(50),
    user_phone VARCHAR(20),
    user_address TEXT,
    wheelchair_id INTEGER,
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 创建临时预订单表索引
CREATE INDEX idx_temp_order_create_time ON temp_order(create_time);
CREATE INDEX idx_temp_order_wheelchair ON temp_order(wheelchair_id);

-- 插入初始轮椅数据
INSERT INTO wheelchair (name, description, price, stock, manufacturer) VALUES
('电动轮椅豪华版', '配备GPS定位、智能刹车系统的高端电动轮椅，适合长期使用', 200.0, 3, '智能康复设备有限公司'),
('手动轮椅标准版', '轻便耐用的手动轮椅，适合日常使用，操作简单', 80.0, 5, '康复器械制造厂'),
('电动轮椅经济版', '性价比高的电动轮椅，操作简单，续航能力强', 120.0, 4, '医疗设备公司'),
('折叠轮椅便携版', '可折叠设计，方便携带和存储，重量轻便', 100.0, 6, '便民医疗器械'),
('多功能电动轮椅', '集成多种辅助功能的电动轮椅，适合重度失能用户', 300.0, 2, '高端医疗器械公司');

-- 插入初始管理员账号 (密码: 123456)
-- 密码哈希值通过 bcrypt 生成
INSERT INTO admin_user (username, password_hash, role) VALUES
('admin', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj6hsxq5S/kS', 'admin'),
('operator1', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj6hsxq5S/kS', 'operator');

-- 插入一些示例订单数据
INSERT INTO formal_order (order_no, user_name, user_phone, user_address, wheelchair_id, deposit, status) VALUES
('WR20250915001', '张三', '13800138001', '北京市朝阳区建国路1号', 1, 200.0, '已完成'),
('WR20250914002', '李四', '13800138002', '上海市浦东新区陆家嘴路2号', 2, 80.0, '待配送'),
('WR20250913003', '王五', '13800138003', '广州市天河区珠江路3号', 3, 120.0, '配送中');

-- 插入一些操作日志数据
INSERT INTO operation_log (operator_id, operate_type, target_id) VALUES
(1, '新增库存', 1),
(1, '新增库存', 2),
(1, '新增库存', 3),
(1, '新增库存', 4),
(1, '新增库存', 5),
(2, '修改订单状态', 1),
(2, '修改订单状态', 2);

-- 数据库初始化完成
SELECT 'Database initialized successfully!' as message;