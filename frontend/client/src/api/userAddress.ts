import axios from 'axios';
import { useUserStore } from '@/stores/user';

/**
 * 创建axios实例
 */
const api = axios.create({
  baseURL: '/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

/**
 * 请求拦截器添加token
 */
api.interceptors.request.use(
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

/**
 * 用户地址信息接口
 */
export interface UserAddress {
  id: number;
  name: string;
  phone: string;
  address: string;
  is_default: boolean;
  create_time: string;
  update_time: string;
}

/**
 * 获取用户所有地址
 */
export const getUserAddresses = async (): Promise<UserAddress[]> => {
  const response = await api.get('/user/address/list');
  return response.data.data;
};

/**
 * 添加新的收货地址
 */
export const addUserAddress = async (
  data: Omit<UserAddress, 'id' | 'create_time' | 'update_time'>
): Promise<UserAddress> => {
  const response = await api.post('/user/address/add', data);
  return response.data;
};

/**
 * 更新收货地址
 */
export const updateUserAddress = async (
  id: number,
  data: Partial<Omit<UserAddress, 'id' | 'create_time' | 'update_time'>>
): Promise<UserAddress> => {
  const response = await api.put(`/user/address/update/${id}`, data);
  return response.data;
};

/**
 * 删除收货地址
 */
export const deleteUserAddress = async (id: number): Promise<void> => {
  await api.delete(`/user/address/delete/${id}`);
};

/**
 * 设置默认收货地址
 */
export const setDefaultAddress = async (id: number): Promise<UserAddress> => {
  const response = await api.post(`/user/address/set_default/${id}`);
  return response.data;
};

/**
 * 获取默认收货地址
 */
export const getDefaultAddress = async (): Promise<UserAddress | null> => {
  const response = await api.get('/user/address/default');
  return response.data;
};