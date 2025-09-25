// API响应基础类型
export interface ApiResponse<T = any> {
  code: number
  message: string
  data?: T
}

// 轮椅类型
export interface Wheelchair {
  id: number
  name: string
  description: string
  price: number
  stock: number
  manufacturer: string
  is_offline?: boolean
  is_deleted?: boolean
}

// 轮椅搜索响应
export interface WheelchairSearchResponse {
  list: Wheelchair[]
  total: number
  page: number
  limit: number
  pages?: number
}

// 轮椅搜索参数
export interface WheelchairSearchParams {
  keyword?: string
  sort_type?: 'price_asc' | 'price_desc'
  page?: number
  limit?: number
}

// 订单类型
export interface Order {
  id: number
  order_no: string
  user_name: string
  user_phone: string
  user_address: string
  wheelchair_id: number
  wheelchair_name?: string
  deposit: number
  status: string
  create_time: string
}

// 临时订单类型
export interface TempOrder {
  id: string
  user_name: string
  user_phone: string
  user_address: string
  wheelchair_id: number
  create_time: string
  expire_time: string
}

// 创建预订单参数
export interface CreateTempOrderParams {
  name: string
  phone: string
  address: string
  wheelchair_id: number
}

// 创建预订单响应
export interface CreateTempOrderResponse {
  pre_order_id: string
  expire_time: string
  wheelchair: Wheelchair
}

// 提交订单参数
export interface SubmitOrderParams {
  pre_order_id: string
}

// 提交订单响应
export interface SubmitOrderResponse {
  order_no: string
  order_id: number
  message: string
  order_info: Order
}