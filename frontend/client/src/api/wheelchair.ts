import axios from "axios";
import type {
  ApiResponse,
  Wheelchair,
  WheelchairSearchResponse,
  WheelchairSearchParams,
  CreateTempOrderParams,
  CreateTempOrderResponse,
  SubmitOrderParams,
  SubmitOrderResponse,
  Order,
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
    // 可以在这里添加loading状态
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

// 轮椅相关API
export const wheelchairApi = {
  // 搜索轮椅
  search: (
    params: WheelchairSearchParams
  ): Promise<ApiResponse<WheelchairSearchResponse>> => {
    return api.get("/wheelchair/search", { params });
  },

  // 获取轮椅详情
  getDetail: (id: number): Promise<ApiResponse<Wheelchair>> => {
    return api.get(`/wheelchair/detail/${id}`);
  },
};

// 订单相关API
export const orderApi = {
  // 创建预订单
  createTempOrder: (
    data: CreateTempOrderParams
  ): Promise<ApiResponse<CreateTempOrderResponse>> => {
    return api.post("/order/precreate", data);
  },

  // 提交正式订单
  submitOrder: (
    data: SubmitOrderParams
  ): Promise<ApiResponse<SubmitOrderResponse>> => {
    return api.post("/order/submit", data);
  },

  // 获取订单详情
  getOrderDetail: (orderNo: string): Promise<ApiResponse<Order>> => {
    return api.get(`/order/detail/${orderNo}`);
  },
};

export default api;
