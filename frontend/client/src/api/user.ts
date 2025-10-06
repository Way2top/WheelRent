import axios from "axios";
import type {
  ApiResponse,
  User,
  LoginParams,
  RegisterParams,
  LoginResponse
} from "@/types/api";

// 创建axios实例
const api = axios.create({
  baseURL: "/api",
  timeout: 10000,
  headers: {
    "Content-Type": "application/json",
  },
});

// 请求拦截器
api.interceptors.request.use(
  (config) => {
    // 添加token认证
    const token = localStorage.getItem('token');
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
api.interceptors.response.use(
  (response) => {
    return response.data;
  },
  (error) => {
    // 统一错误处理
    const message = 
      error.response?.data?.message || error.message || "请求失败";
    console.error("API Error:", message);
    return Promise.reject(new Error(message));
  }
);

// 用户相关API
export const userApi = {
  // 用户注册
  register: (data: RegisterParams): Promise<ApiResponse<LoginResponse>> => {
    return api.post("/user/register", data);
  },

  // 用户登录
  login: (data: LoginParams): Promise<ApiResponse<LoginResponse>> => {
    return api.post("/user/login", data);
  },

  // 获取用户信息
  getUserInfo: (): Promise<ApiResponse<User>> => {
    return api.get("/user/info");
  }
};

export default userApi;