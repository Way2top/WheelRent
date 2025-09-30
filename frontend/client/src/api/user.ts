import axios from "axios";
import type {
  ApiResponse,
  User,
  LoginParams,
  RegisterParams,
  LoginResponse
} from "@/types/api";

// 使用与wheelchair.ts相同的axios实例
import api from "./wheelchair";

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