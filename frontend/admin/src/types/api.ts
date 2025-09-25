// API响应基础接口
export interface ApiResponse<T = any> {
  code: number
  message: string
  data?: T
}

// 分页响应接口
export interface PaginatedResponse<T> {
  items: T[]
  total: number
  page: number
  limit: number
  totalPages: number
}

// 管理员用户接口
export interface AdminUser {
  id: number
  username: string
  email?: string
  role: string
  created_at: string
  last_login?: string
}

// 登录请求接口
export interface LoginRequest {
  username: string
  password: string
}

// 登录响应接口
export interface LoginResponse {
  token: string
  user: AdminUser
}

// 轮椅接口
export interface Wheelchair {
  id: number
  name: string
  description: string
  manufacturer: string
  price: number
  stock: number
  status: 'available' | 'maintenance' | 'discontinued'
  created_at: string
  updated_at: string
}

// 轮椅创建/更新请求接口
export interface WheelchairRequest {
  name: string
  description: string
  manufacturer: string
  price: number
  stock: number
  status: 'available' | 'maintenance' | 'discontinued'
}

// 订单接口
export interface Order {
  id: number
  order_no: string
  user_name: string
  user_phone: string
  user_address: string
  wheelchair_id: number
  wheelchair_name: string
  deposit: number
  status: '待配送' | '已配送' | '使用中' | '已归还' | '已取消'
  create_time: string
  delivery_time?: string
  return_time?: string
  notes?: string
}

// 订单状态更新请求接口
export interface OrderStatusUpdateRequest {
  status: '待配送' | '已配送' | '使用中' | '已归还' | '已取消'
  notes?: string
}

// 用户接口（租赁用户）
export interface User {
  id: number
  name: string
  phone: string
  address: string
  total_orders: number
  active_orders: number
  created_at: string
  last_order_time?: string
}

// 统计数据接口
export interface DashboardStats {
  total_wheelchairs: number
  available_wheelchairs: number
  total_orders: number
  active_orders: number
  total_users: number
  monthly_revenue: number
  daily_orders: Array<{
    date: string
    count: number
  }>
  wheelchair_usage: Array<{
    name: string
    usage_count: number
  }>
  order_status_distribution: Array<{
    status: string
    count: number
  }>
}

// 搜索参数接口
export interface SearchParams {
  page?: number
  limit?: number
  keyword?: string
  status?: string
  start_date?: string
  end_date?: string
}

// 系统设置接口
export interface SystemSettings {
  site_name: string
  contact_phone: string
  contact_email: string
  service_hours: string
  delivery_fee: number
  max_rental_days: number
  deposit_rate: number
  maintenance_mode: boolean
}