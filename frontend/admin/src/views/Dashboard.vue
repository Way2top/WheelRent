<template>
  <div class="dashboard-container">
    <!-- 统计卡片 -->
    <el-row :gutter="20" class="stats-row">
      <el-col :xs="12" :sm="6">
        <el-card class="stats-card">
          <div class="stats-content">
            <div class="stats-icon wheelchair">
              <el-icon size="32"><ShoppingCart /></el-icon>
            </div>
            <div class="stats-info">
              <div class="stats-number">{{ dashboardData.total_wheelchairs || 0 }}</div>
              <div class="stats-label">总轮椅数</div>
            </div>
          </div>
        </el-card>
      </el-col>
      
      <el-col :xs="12" :sm="6">
        <el-card class="stats-card">
          <div class="stats-content">
            <div class="stats-icon available">
              <el-icon size="32"><CircleCheck /></el-icon>
            </div>
            <div class="stats-info">
              <div class="stats-number">{{ dashboardData.available_wheelchairs || 0 }}</div>
              <div class="stats-label">可用轮椅</div>
            </div>
          </div>
        </el-card>
      </el-col>
      
      <el-col :xs="12" :sm="6">
        <el-card class="stats-card">
          <div class="stats-content">
            <div class="stats-icon orders">
              <el-icon size="32"><Document /></el-icon>
            </div>
            <div class="stats-info">
              <div class="stats-number">{{ dashboardData.total_orders || 0 }}</div>
              <div class="stats-label">总订单数</div>
            </div>
          </div>
        </el-card>
      </el-col>
      
      <el-col :xs="12" :sm="6">
        <el-card class="stats-card">
          <div class="stats-content">
            <div class="stats-icon users">
              <el-icon size="32"><User /></el-icon>
            </div>
            <div class="stats-info">
              <div class="stats-number">{{ dashboardData.total_users || 0 }}</div>
              <div class="stats-label">总用户数</div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
    
    <!-- 图表区域 -->
    <el-row :gutter="20" class="charts-row">
      <!-- 订单趋势图 -->
      <el-col :xs="24" :lg="12">
        <el-card class="chart-card">
          <template #header>
            <div class="card-header">
              <span>订单趋势</span>
              <el-button type="text" @click="refreshOrderTrend">
                <el-icon><Refresh /></el-icon>
              </el-button>
            </div>
          </template>
          
          <div class="chart-container">
            <v-chart
              v-if="orderTrendOption"
              :option="orderTrendOption"
              :style="{ height: '300px' }"
              autoresize
            />
            <el-skeleton v-else :rows="6" animated />
          </div>
        </el-card>
      </el-col>
      
      <!-- 轮椅使用统计 -->
      <el-col :xs="24" :lg="12">
        <el-card class="chart-card">
          <template #header>
            <div class="card-header">
              <span>轮椅使用统计</span>
              <el-button type="text" @click="refreshWheelchairUsage">
                <el-icon><Refresh /></el-icon>
              </el-button>
            </div>
          </template>
          
          <div class="chart-container">
            <v-chart
              v-if="wheelchairUsageOption"
              :option="wheelchairUsageOption"
              :style="{ height: '300px' }"
              autoresize
            />
            <el-skeleton v-else :rows="6" animated />
          </div>
        </el-card>
      </el-col>
    </el-row>
    
    <!-- 订单状态分布 -->
    <el-row :gutter="20" class="charts-row">
      <el-col :xs="24" :lg="8">
        <el-card class="chart-card">
          <template #header>
            <div class="card-header">
              <span>订单状态分布</span>
              <el-button type="text" @click="refreshOrderStatus">
                <el-icon><Refresh /></el-icon>
              </el-button>
            </div>
          </template>
          
          <div class="chart-container">
            <v-chart
              v-if="orderStatusOption"
              :option="orderStatusOption"
              :style="{ height: '300px' }"
              autoresize
            />
            <el-skeleton v-else :rows="6" animated />
          </div>
        </el-card>
      </el-col>
      
      <!-- 最近活动 -->
      <el-col :xs="24" :lg="16">
        <el-card class="activity-card">
          <template #header>
            <div class="card-header">
              <span>最近活动</span>
              <el-button type="text" @click="refreshActivities">
                <el-icon><Refresh /></el-icon>
              </el-button>
            </div>
          </template>
          
          <div class="activity-list">
            <el-timeline>
              <el-timeline-item
                v-for="(activity, index) in recentActivities"
                :key="index"
                :timestamp="activity.time"
                :type="activity.type"
              >
                <div class="activity-content">
                  <div class="activity-title">{{ activity.title }}</div>
                  <div class="activity-desc">{{ activity.description }}</div>
                </div>
              </el-timeline-item>
            </el-timeline>
            
            <div v-if="recentActivities.length === 0" class="empty-activities">
              <el-empty description="暂无活动记录" :image-size="80" />
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { ElMessage } from 'element-plus'
import {
  ShoppingCart,
  CircleCheck,
  Document,
  User,
  Refresh
} from '@element-plus/icons-vue'
import VChart from 'vue-echarts'
import { use } from 'echarts/core'
import {
  CanvasRenderer
} from 'echarts/renderers'
import {
  LineChart,
  BarChart,
  PieChart
} from 'echarts/charts'
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent
} from 'echarts/components'
import { dashboardApi } from '@/api'
import type { DashboardStats } from '@/types/api'

// 注册ECharts组件
use([
  CanvasRenderer,
  LineChart,
  BarChart,
  PieChart,
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent
])

// 响应式数据
const loading = ref(false)
const dashboardData = ref<DashboardStats>({
  total_wheelchairs: 0,
  available_wheelchairs: 0,
  total_orders: 0,
  active_orders: 0,
  total_users: 0,
  monthly_revenue: 0,
  daily_orders: [],
  wheelchair_usage: [],
  order_status_distribution: []
})

// 最近活动数据
const recentActivities = ref([
  {
    time: '2024-01-15 14:30',
    type: 'primary',
    title: '新订单创建',
    description: '用户张三创建了轮椅租赁订单 #WR20240115001'
  },
  {
    time: '2024-01-15 13:45',
    type: 'success',
    title: '订单完成',
    description: '订单 #WR20240114005 已完成归还，轮椅状态已更新'
  },
  {
    time: '2024-01-15 12:20',
    type: 'warning',
    title: '库存预警',
    description: '标准轮椅库存不足，当前剩余 3 台'
  },
  {
    time: '2024-01-15 11:15',
    type: 'info',
    title: '新用户注册',
    description: '新用户李四完成注册，用户总数达到 156 人'
  },
  {
    time: '2024-01-15 10:30',
    type: 'success',
    title: '轮椅维护完成',
    description: '电动轮椅 #EW001 维护完成，已重新上架'
  }
])

// 订单趋势图配置
const orderTrendOption = computed(() => {
  if (!dashboardData.value.daily_orders.length) return null
  
  return {
    title: {
      text: '近30天订单趋势',
      textStyle: {
        fontSize: 14,
        fontWeight: 'normal'
      }
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'cross'
      }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: dashboardData.value.daily_orders.map(item => item.date)
    },
    yAxis: {
      type: 'value'
    },
    series: [
      {
        name: '订单数量',
        type: 'line',
        smooth: true,
        data: dashboardData.value.daily_orders.map(item => item.count),
        itemStyle: {
          color: '#409EFF'
        },
        areaStyle: {
          color: {
            type: 'linear',
            x: 0,
            y: 0,
            x2: 0,
            y2: 1,
            colorStops: [
              {
                offset: 0,
                color: 'rgba(64, 158, 255, 0.3)'
              },
              {
                offset: 1,
                color: 'rgba(64, 158, 255, 0.1)'
              }
            ]
          }
        }
      }
    ]
  }
})

// 轮椅使用统计配置
const wheelchairUsageOption = computed(() => {
  if (!dashboardData.value.wheelchair_usage.length) return null
  
  return {
    title: {
      text: '轮椅使用排行',
      textStyle: {
        fontSize: 14,
        fontWeight: 'normal'
      }
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'value'
    },
    yAxis: {
      type: 'category',
      data: dashboardData.value.wheelchair_usage.map(item => item.name)
    },
    series: [
      {
        name: '使用次数',
        type: 'bar',
        data: dashboardData.value.wheelchair_usage.map(item => item.usage_count),
        itemStyle: {
          color: '#67C23A'
        }
      }
    ]
  }
})

// 订单状态分布配置
const orderStatusOption = computed(() => {
  if (!dashboardData.value.order_status_distribution.length) return null
  
  return {
    title: {
      text: '订单状态分布',
      textStyle: {
        fontSize: 14,
        fontWeight: 'normal'
      },
      left: 'center'
    },
    tooltip: {
      trigger: 'item',
      formatter: '{a} <br/>{b}: {c} ({d}%)'
    },
    legend: {
      orient: 'vertical',
      left: 'left',
      top: 'middle'
    },
    series: [
      {
        name: '订单状态',
        type: 'pie',
        radius: ['40%', '70%'],
        center: ['60%', '50%'],
        data: dashboardData.value.order_status_distribution.map(item => ({
          value: item.count,
          name: item.status
        })),
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: 'rgba(0, 0, 0, 0.5)'
          }
        }
      }
    ]
  }
})

// 获取仪表板数据
const getDashboardData = async () => {
  try {
    loading.value = true
    
    // 模拟API调用，实际应该调用 dashboardApi.getStats()
    // const response = await dashboardApi.getStats()
    
    // 模拟数据
    const mockData: DashboardStats = {
      total_wheelchairs: 45,
      available_wheelchairs: 32,
      total_orders: 128,
      active_orders: 15,
      total_users: 89,
      monthly_revenue: 25600,
      daily_orders: [
        { date: '01-01', count: 5 },
        { date: '01-02', count: 8 },
        { date: '01-03', count: 12 },
        { date: '01-04', count: 7 },
        { date: '01-05', count: 15 },
        { date: '01-06', count: 10 },
        { date: '01-07', count: 18 },
        { date: '01-08', count: 14 },
        { date: '01-09', count: 9 },
        { date: '01-10', count: 16 }
      ],
      wheelchair_usage: [
        { name: '标准轮椅', usage_count: 45 },
        { name: '电动轮椅', usage_count: 32 },
        { name: '轻便轮椅', usage_count: 28 },
        { name: '运动轮椅', usage_count: 15 },
        { name: '儿童轮椅', usage_count: 8 }
      ],
      order_status_distribution: [
        { status: '待配送', count: 8 },
        { status: '已配送', count: 5 },
        { status: '使用中', count: 15 },
        { status: '已归还', count: 95 },
        { status: '已取消', count: 5 }
      ]
    }
    
    dashboardData.value = mockData
  } catch (error) {
    console.error('获取仪表板数据失败:', error)
    ElMessage.error('获取数据失败，请稍后重试')
  } finally {
    loading.value = false
  }
}

// 刷新订单趋势
const refreshOrderTrend = () => {
  ElMessage.success('订单趋势数据已刷新')
  getDashboardData()
}

// 刷新轮椅使用统计
const refreshWheelchairUsage = () => {
  ElMessage.success('轮椅使用统计已刷新')
  getDashboardData()
}

// 刷新订单状态
const refreshOrderStatus = () => {
  ElMessage.success('订单状态分布已刷新')
  getDashboardData()
}

// 刷新活动记录
const refreshActivities = () => {
  ElMessage.success('活动记录已刷新')
  // 这里可以重新获取活动数据
}

// 组件挂载时获取数据
onMounted(() => {
  getDashboardData()
})
</script>

<style scoped>
.dashboard-container {
  padding: 0;
}

.stats-row {
  margin-bottom: 20px;
}

.charts-row {
  margin-bottom: 20px;
}

.stats-card {
  border-radius: 8px;
  overflow: hidden;
}

.stats-content {
  display: flex;
  align-items: center;
  gap: 16px;
}

.stats-icon {
  width: 60px;
  height: 60px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.stats-icon.wheelchair {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.stats-icon.available {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
}

.stats-icon.orders {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
}

.stats-icon.users {
  background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
}

.stats-info {
  flex: 1;
}

.stats-number {
  font-size: 28px;
  font-weight: 600;
  color: #2c3e50;
  line-height: 1;
  margin-bottom: 4px;
}

.stats-label {
  font-size: 14px;
  color: #7f8c8d;
}

.chart-card,
.activity-card {
  border-radius: 8px;
  overflow: hidden;
}

.chart-container {
  padding: 10px 0;
}

.activity-list {
  max-height: 300px;
  overflow-y: auto;
}

.activity-content {
  padding-left: 10px;
}

.activity-title {
  font-size: 14px;
  font-weight: 500;
  color: #2c3e50;
  margin-bottom: 4px;
}

.activity-desc {
  font-size: 12px;
  color: #7f8c8d;
  line-height: 1.4;
}

.empty-activities {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 200px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .stats-content {
    gap: 12px;
  }
  
  .stats-icon {
    width: 48px;
    height: 48px;
  }
  
  .stats-icon .el-icon {
    font-size: 24px !important;
  }
  
  .stats-number {
    font-size: 24px;
  }
  
  .stats-label {
    font-size: 12px;
  }
}
</style>