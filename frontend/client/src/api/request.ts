import axios from 'axios';
import { useUserStore } from '@/stores/user';

// 创建axios实例
const request = axios.create({
  baseURL: '/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// 请求拦截器
request.interceptors.request.use(
  (config) => {
    const userStore = useUserStore();
    const token = userStore.token;
    
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// 响应拦截器
request.interceptors.response.use(
  (response) => {
    // 假设后端返回的格式是 { code: number, message: string, data?: any }
    return response.data;
  },
  (error) => {
    console.error('请求错误:', error);
    return Promise.reject(error);
  }
);

export default request;