<template>
  <div class="order-management">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>订单管理</span>
          <el-button type="primary" @click="handleExport">
            <el-icon><Download /></el-icon>
            导出订单
          </el-button>
        </div>
      </template>
      
      <!-- 搜索工具栏 -->
      <div class="table-toolbar">
        <div class="search-form">
          <el-input
            v-model="searchParams.keyword"
            placeholder="搜索订单号或用户姓名"
            style="width: 240px;"
            clearable
            @keyup.enter="handleSearch"
          >
            <template #prefix>
              <el-icon><Search /></el-icon>
            </template>
          </el-input>
          
          <el-select
            v-model="searchParams.status"
            placeholder="状态筛选"
            style="width: 120px;"
            clearable
          >
            <el-option label="待配送" value="待配送" />
            <el-option label="已配送" value="已配送" />
            <el-option label="使用中" value="使用中" />
            <el-option label="已归还" value="已归还" />
            <el-option label="已取消" value="已取消" />
          </el-select>
          
          <el-date-picker
            v-model="dateRange"
            type="daterange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            format="YYYY-MM-DD"
            value-format="YYYY-MM-DD"
            @change="handleDateChange"
          />
          
          <el-button type="primary" @click="handleSearch">
            <el-icon><Search /></el-icon>
            搜索
          </el-button>
          
          <el-button @click="handleReset">
            <el-icon><Refresh /></el-icon>
            重置
          </el-button>
        </div>
      </div>
      
      <!-- 数据表格 -->
      <el-table
        v-loading="loading"
        :data="tableData"
        stripe
        style="width: 100%"
      >
        <el-table-column prop="id" label="ID" width="80" />
        
        <el-table-column prop="order_no" label="订单号" width="180">
          <template #default="{ row }">
            <el-button type="text" @click="handleViewDetail(row)">
              {{ row.order_no }}
            </el-button>
          </template>
        </el-table-column>
        
        <el-table-column label="用户信息" min-width="150">
          <template #default="{ row }">
            <div class="user-info">
              <div class="user-name">{{ row.user_name }}</div>
              <div class="user-phone">{{ row.user_phone }}</div>
            </div>
          </template>
        </el-table-column>
        
        <el-table-column prop="wheelchair_name" label="轮椅" min-width="120" />
        
        <el-table-column prop="deposit" label="定金" width="100">
          <template #default="{ row }">
            <span class="price">¥{{ row.deposit }}</span>
          </template>
        </el-table-column>
        
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag
              :type="getStatusType(row.status)"
              size="small"
            >
              {{ row.status }}
            </el-tag>
          </template>
        </el-table-column>
        
        <el-table-column prop="create_time" label="下单时间" width="180">
          <template #default="{ row }">
            {{ formatTime(row.create_time) }}
          </template>
        </el-table-column>
        
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button type="text" size="small" @click="handleViewDetail(row)">
              <el-icon><View /></el-icon>
              详情
            </el-button>
            
            <el-button
              v-if="canUpdateStatus(row.status)"
              type="text"
              size="small"
              @click="handleUpdateStatus(row)"
            >
              <el-icon><Edit /></el-icon>
              更新状态
            </el-button>
            
            <el-button
              v-if="canCancel(row.status)"
              type="text"
              size="small"
              style="color: #f56c6c;"
              @click="handleCancel(row)"
            >
              <el-icon><Close /></el-icon>
              取消
            </el-button>
          </template>
        </el-table-column>
      </el-table>
      
      <!-- 分页 -->
      <div class="pagination-container">
        <el-pagination
          v-model:current-page="searchParams.page"
          v-model:page-size="searchParams.limit"
          :total="total"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>
    
    <!-- 订单详情对话框 -->
    <el-dialog
      v-model="detailDialogVisible"
      title="订单详情"
      width="800px"
    >
      <div v-if="currentOrder" class="order-detail">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="订单号">{{ currentOrder.order_no }}</el-descriptions-item>
          <el-descriptions-item label="订单状态">
            <el-tag :type="getStatusType(currentOrder.status)">
              {{ currentOrder.status }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="用户姓名">{{ currentOrder.user_name }}</el-descriptions-item>
          <el-descriptions-item label="联系电话">{{ currentOrder.user_phone }}</el-descriptions-item>
          <el-descriptions-item label="收货地址" :span="2">{{ currentOrder.user_address }}</el-descriptions-item>
          <el-descriptions-item label="轮椅名称">{{ currentOrder.wheelchair_name }}</el-descriptions-item>
          <el-descriptions-item label="定金金额">
            <span class="price">¥{{ currentOrder.deposit }}</span>
          </el-descriptions-item>
          <el-descriptions-item label="下单时间">{{ formatTime(currentOrder.create_time) }}</el-descriptions-item>
          <el-descriptions-item label="配送时间">
            {{ currentOrder.delivery_time ? formatTime(currentOrder.delivery_time) : '未配送' }}
          </el-descriptions-item>
          <el-descriptions-item label="归还时间">
            {{ currentOrder.return_time ? formatTime(currentOrder.return_time) : '未归还' }}
          </el-descriptions-item>
          <el-descriptions-item label="备注" :span="2">
            {{ currentOrder.notes || '无' }}
          </el-descriptions-item>
        </el-descriptions>
      </div>
    </el-dialog>
    
    <!-- 更新状态对话框 -->
    <el-dialog
      v-model="statusDialogVisible"
      title="更新订单状态"
      width="400px"
    >
      <el-form
        ref="statusFormRef"
        :model="statusForm"
        :rules="statusRules"
        label-width="80px"
      >
        <el-form-item label="新状态" prop="status">
          <el-select v-model="statusForm.status" style="width: 100%;">
            <el-option label="待配送" value="待配送" />
            <el-option label="已配送" value="已配送" />
            <el-option label="使用中" value="使用中" />
            <el-option label="已归还" value="已归还" />
            <el-option label="已取消" value="已取消" />
          </el-select>
        </el-form-item>
        
        <el-form-item label="备注" prop="notes">
          <el-input
            v-model="statusForm.notes"
            type="textarea"
            :rows="3"
            placeholder="请输入备注信息（可选）"
          />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <el-button @click="statusDialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="statusLoading" @click="handleStatusSubmit">
          确定更新
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox, type FormInstance, type FormRules } from 'element-plus'
import {
  Download,
  Search,
  Refresh,
  View,
  Edit,
  Close
} from '@element-plus/icons-vue'
import { orderApi } from '@/api'
import type { Order, OrderStatusUpdateRequest, SearchParams } from '@/types/api'

// 响应式数据
const loading = ref(false)
const statusLoading = ref(false)
const detailDialogVisible = ref(false)
const statusDialogVisible = ref(false)
const statusFormRef = ref<FormInstance>()
const tableData = ref<Order[]>([])
const currentOrder = ref<Order | null>(null)
const currentOrderId = ref<number | null>(null)
const total = ref(0)
const dateRange = ref<[string, string] | null>(null)

// 搜索参数
const searchParams = reactive<SearchParams>({
  page: 1,
  limit: 20,
  keyword: '',
  status: '',
  start_date: '',
  end_date: ''
})

// 状态更新表单
const statusForm = reactive<OrderStatusUpdateRequest>({
  status: '待配送',
  notes: ''
})

// 状态表单验证规则
const statusRules: FormRules = {
  status: [
    { required: true, message: '请选择订单状态', trigger: 'change' }
  ]
}

// 获取状态类型
const getStatusType = (status: string) => {
  const typeMap: Record<string, string> = {
    '待配送': 'warning',
    '已配送': 'primary',
    '使用中': 'success',
    '已归还': 'info',
    '已取消': 'danger'
  }
  return typeMap[status] || 'info'
}

// 格式化时间
const formatTime = (timeStr: string) => {
  const date = new Date(timeStr)
  return date.toLocaleString('zh-CN')
}

// 判断是否可以更新状态
const canUpdateStatus = (status: string) => {
  return !['已归还', '已取消'].includes(status)
}

// 判断是否可以取消
const canCancel = (status: string) => {
  return ['待配送', '已配送'].includes(status)
}

// 处理日期范围变化
const handleDateChange = (dates: [string, string] | null) => {
  if (dates) {
    searchParams.start_date = dates[0]
    searchParams.end_date = dates[1]
  } else {
    searchParams.start_date = ''
    searchParams.end_date = ''
  }
}

// 获取订单列表
const getOrderList = async () => {
  try {
    loading.value = true
    
    // 模拟API调用
    // const response = await orderApi.getList(searchParams)
    
    // 模拟数据
    const mockData = {
      items: [
        {
          id: 1,
          order_no: 'WR20250915001',
          user_name: '张三',
          user_phone: '13800138001',
          user_address: '北京市朝阳区某某街道123号',
          wheelchair_id: 1,
          wheelchair_name: '标准轮椅 SW-001',
          deposit: 50,
          status: '使用中',
          create_time: '2025-09-15T10:30:00Z',
delivery_time: '2025-09-15T14:30:00Z',
          return_time: null,
          notes: '用户要求下午配送'
        },
        {
          id: 2,
          order_no: 'WR20250915002',
          user_name: '李四',
          user_phone: '13800138002',
          user_address: '上海市浦东新区某某路456号',
          wheelchair_id: 2,
          wheelchair_name: '电动轮椅 EW-002',
          deposit: 120,
          status: '待配送',
          create_time: '2025-09-15T11:00:00Z',
          delivery_time: null,
          return_time: null,
          notes: null
        },
        {
          id: 3,
          order_no: 'WR20250914003',
          user_name: '王五',
          user_phone: '13800138003',
          user_address: '广州市天河区某某大道789号',
          wheelchair_id: 1,
          wheelchair_name: '标准轮椅 SW-001',
          deposit: 50,
          status: '已归还',
          create_time: '2025-09-14T09:00:00Z',
delivery_time: '2025-09-14T13:00:00Z',
return_time: '2025-09-15T09:00:00Z',
          notes: '按时归还，轮椅状态良好'
        }
      ],
      total: 3,
      page: 1,
      limit: 20,
      totalPages: 1
    }
    
    tableData.value = mockData.items
    total.value = mockData.total
  } catch (error) {
    console.error('获取订单列表失败:', error)
    ElMessage.error('获取数据失败，请稍后重试')
  } finally {
    loading.value = false
  }
}

// 搜索
const handleSearch = () => {
  searchParams.page = 1
  getOrderList()
}

// 重置
const handleReset = () => {
  Object.assign(searchParams, {
    page: 1,
    limit: 20,
    keyword: '',
    status: '',
    start_date: '',
    end_date: ''
  })
  dateRange.value = null
  getOrderList()
}

// 导出订单
const handleExport = async () => {
  try {
    ElMessage.info('导出功能开发中...')
    // const blob = await orderApi.export(searchParams)
    // 创建下载链接
    // const url = window.URL.createObjectURL(blob)
    // const link = document.createElement('a')
    // link.href = url
    // link.download = `orders_${new Date().getTime()}.xlsx`
    // link.click()
    // window.URL.revokeObjectURL(url)
  } catch (error) {
    console.error('导出失败:', error)
    ElMessage.error('导出失败，请稍后重试')
  }
}

// 分页大小变化
const handleSizeChange = (size: number) => {
  searchParams.limit = size
  searchParams.page = 1
  getOrderList()
}

// 当前页变化
const handleCurrentChange = (page: number) => {
  searchParams.page = page
  getOrderList()
}

// 查看详情
const handleViewDetail = async (row: Order) => {
  try {
    // 模拟API调用获取详细信息
    // const response = await orderApi.getDetail(row.id)
    // currentOrder.value = response.data
    
    currentOrder.value = row
    detailDialogVisible.value = true
  } catch (error) {
    console.error('获取订单详情失败:', error)
    ElMessage.error('获取订单详情失败')
  }
}

// 更新状态
const handleUpdateStatus = (row: Order) => {
  currentOrderId.value = row.id
  statusForm.status = row.status as any
  statusForm.notes = ''
  statusDialogVisible.value = true
}

// 取消订单
const handleCancel = async (row: Order) => {
  try {
    await ElMessageBox.confirm(
      `确定要取消订单"${row.order_no}"吗？`,
      '取消订单确认',
      {
        confirmButtonText: '确定取消',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    // 模拟API调用
    // await orderApi.updateStatus(row.id, { status: '已取消', notes: '管理员取消' })
    
    ElMessage.success('订单已取消')
    getOrderList()
  } catch (error: any) {
    if (error !== 'cancel') {
      console.error('取消订单失败:', error)
      ElMessage.error('取消订单失败，请稍后重试')
    }
  }
}

// 提交状态更新
const handleStatusSubmit = async () => {
  if (!statusFormRef.value || !currentOrderId.value) return
  
  try {
    const valid = await statusFormRef.value.validate()
    if (!valid) return
    
    statusLoading.value = true
    
    // 模拟API调用
    // await orderApi.updateStatus(currentOrderId.value, statusForm)
    
    ElMessage.success('状态更新成功')
    statusDialogVisible.value = false
    getOrderList()
  } catch (error) {
    console.error('状态更新失败:', error)
    ElMessage.error('状态更新失败，请稍后重试')
  } finally {
    statusLoading.value = false
  }
}

// 组件挂载时获取数据
onMounted(() => {
  getOrderList()
})
</script>

<style scoped>
.order-management {
  padding: 0;
}

.table-toolbar {
  margin-bottom: 20px;
}

.search-form {
  display: flex;
  gap: 16px;
  align-items: center;
  flex-wrap: wrap;
}

.user-info {
  line-height: 1.4;
}

.user-name {
  font-weight: 500;
  color: #2c3e50;
  margin-bottom: 2px;
}

.user-phone {
  font-size: 12px;
  color: #7f8c8d;
}

.price {
  font-weight: 600;
  color: #e74c3c;
}

.pagination-container {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

.order-detail {
  padding: 10px 0;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .search-form {
    justify-content: center;
  }
}
</style>