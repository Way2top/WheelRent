import { defineStore } from 'pinia'
import { ref } from 'vue'
import { userApi } from '@/api/user'
import type { User, LoginParams, RegisterParams } from '@/types/api'

export const useUserStore = defineStore('user', () => {
  const token = ref<string | null>(localStorage.getItem('token'))
  const user = ref<User | null>(null)
  const isLoggedIn = ref(!!token.value)
  const loading = ref(false)

  // 设置token
  const setToken = (newToken: string | null) => {
    token.value = newToken
    if (newToken) {
      localStorage.setItem('token', newToken)
      isLoggedIn.value = true
    } else {
      localStorage.removeItem('token')
      isLoggedIn.value = false
    }
  }

  // 设置用户信息
  const setUser = (newUser: User | null) => {
    user.value = newUser
  }

  // 登录
  const login = async (loginData: LoginParams) => {
    try {
      loading.value = true
      const response = await userApi.login(loginData)
      if (response.code === 200 && response.data) {
        setToken(response.data.token)
        setUser(response.data.user_info)
        return true
      }
      return false
    } catch (error) {
      console.error('登录失败:', error)
      return false
    } finally {
      loading.value = false
    }
  }

  // 注册
  const register = async (registerData: RegisterParams) => {
    try {
      loading.value = true
      const response = await userApi.register(registerData)
      if (response.code === 200 && response.data) {
        setToken(response.data.token)
        setUser(response.data.user_info)
        return true
      }
      return false
    } catch (error) {
      console.error('注册失败:', error)
      return false
    } finally {
      loading.value = false
    }
  }

  // 获取用户信息
  const getUserInfo = async () => {
    if (!token.value) return false
    
    try {
      loading.value = true
      const response = await userApi.getUserInfo()
      if (response.code === 200 && response.data) {
        setUser(response.data)
        return true
      }
      return false
    } catch (error) {
      console.error('获取用户信息失败:', error)
      logout()
      return false
    } finally {
      loading.value = false
    }
  }

  // 登出
  const logout = () => {
    setToken(null)
    setUser(null)
  }

  return {
    token,
    user,
    isLoggedIn,
    loading,
    login,
    register,
    getUserInfo,
    logout
  }
})