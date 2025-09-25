import axios from 'axios'
import { ElMessage } from 'element-plus'
import { useAuthStore } from '@/stores/auth'
import type {
  ApiResponse,
  PaginatedResponse,
  LoginRequest,
  LoginResponse,
  Wheelchair,
  WheelchairRequest,
  Order,
  OrderStatusUpdateRequest,
  User,
  DashboardStats,
  SearchParams,
  SystemSettings
} from '@/types/api'

// 创建axios实例
const api = axios.create({
  baseURL: '/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
api.interceptors.request.use(
  (config) => {
    const authStore = useAuthStore()
    const token = authStore.token
    
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  (response) => {
    return response.data
  },
  (error) => {
    const authStore = useAuthStore()
    
    if (error.response) {
      const { status, data } = error.response
      
      switch (status) {
        case 401:
          ElMessage.error('登录已过期，请重新登录')
          authStore.logout()
          window.location.href = '/login'
          break
        case 403:
          ElMessage.error('没有权限访问该资源')
          break
        case 404:
          ElMessage.error('请求的资源不存在')
          break
        case 500:
          ElMessage.error('服务器内部错误')
          break
        default:
          ElMessage.error(data?.message || '请求失败')
      }
    } else if (error.request) {
      ElMessage.error('网络连接失败，请检查网络')
    } else {
      ElMessage.error('请求配置错误')
    }
    
    return Promise.reject(error)
  }
)

// 认证API
export const authApi = {
  // 管理员登录
  login: (data: LoginRequest): Promise<ApiResponse<LoginResponse>> => {
    return api.post('/admin/login', data)
  },
  
  // 获取当前用户信息
  getCurrentUser: (): Promise<ApiResponse<any>> => {
    return api.get('/admin/profile')
  },
  
  // 修改密码
  changePassword: (data: { oldPassword: string; newPassword: string }): Promise<ApiResponse> => {
    return api.post('/admin/change-password', data)
  }
}

// 仪表板API
export const dashboardApi = {
  // 获取统计数据
  getStats: (): Promise<ApiResponse<DashboardStats>> => {
    return api.get('/admin/dashboard/stats')
  }
}

// 轮椅管理API
export const wheelchairApi = {
  // 获取轮椅列表
  getList: (params: SearchParams): Promise<ApiResponse<PaginatedResponse<Wheelchair>>> => {
    return api.get('/admin/wheelchairs', { params })
  },
  
  // 获取轮椅详情
  getDetail: (id: number): Promise<ApiResponse<Wheelchair>> => {
    return api.get(`/admin/wheelchairs/${id}`)
  },
  
  // 创建轮椅
  create: (data: WheelchairRequest): Promise<ApiResponse<Wheelchair>> => {
    return api.post('/admin/wheelchairs', data)
  },
  
  // 更新轮椅
  update: (id: number, data: WheelchairRequest): Promise<ApiResponse<Wheelchair>> => {
    return api.put(`/admin/wheelchairs/${id}`, data)
  },
  
  // 删除轮椅
  delete: (id: number): Promise<ApiResponse> => {
    return api.delete(`/admin/wheelchairs/${id}`)
  },
  
  // 批量更新状态
  batchUpdateStatus: (ids: number[], status: string): Promise<ApiResponse> => {
    return api.post('/admin/wheelchairs/batch-status', { ids, status })
  }
}

// 订单管理API
export const orderApi = {
  // 获取订单列表
  getList: (params: SearchParams): Promise<ApiResponse<PaginatedResponse<Order>>> => {
    return api.get('/admin/orders', { params })
  },
  
  // 获取订单详情
  getDetail: (id: number): Promise<ApiResponse<Order>> => {
    return api.get(`/admin/orders/${id}`)
  },
  
  // 更新订单状态
  updateStatus: (id: number, data: OrderStatusUpdateRequest): Promise<ApiResponse<Order>> => {
    return api.put(`/admin/orders/${id}/status`, data)
  },
  
  // 删除订单
  delete: (id: number): Promise<ApiResponse> => {
    return api.delete(`/admin/orders/${id}`)
  },
  
  // 导出订单
  export: (params: SearchParams): Promise<Blob> => {
    return api.get('/admin/orders/export', {
      params,
      responseType: 'blob'
    })
  }
}

// 用户管理API
export const userApi = {
  // 获取用户列表
  getList: (params: SearchParams): Promise<ApiResponse<PaginatedResponse<User>>> => {
    return api.get('/admin/users', { params })
  },
  
  // 获取用户详情
  getDetail: (id: number): Promise<ApiResponse<User>> => {
    return api.get(`/admin/users/${id}`)
  },
  
  // 获取用户订单历史
  getUserOrders: (userId: number, params: SearchParams): Promise<ApiResponse<PaginatedResponse<Order>>> => {
    return api.get(`/admin/users/${userId}/orders`, { params })
  }
}

// 系统设置API
export const settingsApi = {
  // 获取系统设置
  getSettings: (): Promise<ApiResponse<SystemSettings>> => {
    return api.get('/admin/settings')
  },
  
  // 更新系统设置
  updateSettings: (data: Partial<SystemSettings>): Promise<ApiResponse<SystemSettings>> => {
    return api.put('/admin/settings', data)
  }
}

export default api