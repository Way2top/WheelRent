import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { AdminUser } from '@/types/api'

export const useAuthStore = defineStore('auth', () => {
  // 状态
  const token = ref<string | null>(localStorage.getItem('admin_token'))
  const user = ref<AdminUser | null>(null)
  const loading = ref(false)

  // 计算属性
  const isLoggedIn = computed(() => {
    return !!token.value && !!user.value
  })

  // 登录
  const login = (tokenValue: string, userData: AdminUser) => {
    token.value = tokenValue
    user.value = userData
    localStorage.setItem('admin_token', tokenValue)
    localStorage.setItem('admin_user', JSON.stringify(userData))
  }

  // 登出
  const logout = () => {
    token.value = null
    user.value = null
    localStorage.removeItem('admin_token')
    localStorage.removeItem('admin_user')
  }

  // 初始化用户信息
  const initUser = () => {
    const savedUser = localStorage.getItem('admin_user')
    if (savedUser && token.value) {
      try {
        user.value = JSON.parse(savedUser)
      } catch (error) {
        console.error('解析用户信息失败:', error)
        logout()
      }
    }
  }

  // 更新用户信息
  const updateUser = (userData: Partial<AdminUser>) => {
    if (user.value) {
      user.value = { ...user.value, ...userData }
      localStorage.setItem('admin_user', JSON.stringify(user.value))
    }
  }

  // 设置加载状态
  const setLoading = (value: boolean) => {
    loading.value = value
  }

  // 检查token是否有效
  const checkTokenValidity = () => {
    // 这里可以添加token过期检查逻辑
    // 如果token过期，自动登出
    if (token.value) {
      try {
        // 简单的token格式检查
        const parts = token.value.split('.')
        if (parts.length !== 3) {
          logout()
          return false
        }
        return true
      } catch (error) {
        logout()
        return false
      }
    }
    return false
  }

  // 获取认证头
  const getAuthHeader = () => {
    return token.value ? { Authorization: `Bearer ${token.value}` } : {}
  }

  return {
    // 状态
    token,
    user,
    loading,
    
    // 计算属性
    isLoggedIn,
    
    // 方法
    login,
    logout,
    initUser,
    updateUser,
    setLoading,
    checkTokenValidity,
    getAuthHeader
  }
})