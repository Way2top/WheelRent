<template>
  <div class="user-management">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>用户管理</span>
        </div>
      </template>
      
      <!-- 搜索工具栏 -->
      <div class="table-toolbar">
        <div class="search-form">
          <el-input
            v-model="searchParams.keyword"
            placeholder="搜索用户姓名或手机号"
            style="width: 240px;"
            clearable
            @keyup.enter="handleSearch"
          >
            <template #prefix>
              <el-icon><Search /></el-icon>
            </template>
          </el-input>
          
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
        
        <el-table-column label="用户信息" min-width="200">
          <template #default="{ row }">
            <div class="user-info">
              <div class="user-avatar">
                <el-avatar :size="40">
                  <el-icon><User /></el-icon>
                </el-avatar>
              </div>
              <div class="user-details">
                <div class="user-name">{{ row.name }}</div>
                <div class="user-phone">{{ row.phone }}</div>
              </div>
            </div>
          </template>
        </el-table-column>
        
        <el-table-column prop="address" label="地址" min-width="200">
          <template #default="{ row }">
            <el-tooltip :content="row.address" placement="top">
              <div class="address-text">{{ row.address }}</div>
            </el-tooltip>
          </template>
        </el-table-column>
        
        <el-table-column prop="total_orders" label="总订单数" width="100" align="center">
          <template #default="{ row }">
            <el-tag type="info" size="small">
              {{ row.total_orders }}
            </el-tag>
          </template>
        </el-table-column>
        
        <el-table-column prop="active_orders" label="进行中订单" width="120" align="center">
          <template #default="{ row }">
            <el-tag
              :type="row.active_orders > 0 ? 'warning' : 'success'"
              size="small"
            >
              {{ row.active_orders }}
            </el-tag>
          </template>
        </el-table-column>
        
        <el-table-column prop="created_at" label="注册时间" width="180">
          <template #default="{ row }">
            {{ formatTime(row.created_at) }}
          </template>
        </el-table-column>
        
        <el-table-column prop="last_order_time" label="最后下单" width="180">
          <template #default="{ row }">
            {{ row.last_order_time ? formatTime(row.last_order_time) : '无' }}
          </template>
        </el-table-column>
        
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button type="text" size="small" @click="handleViewDetail(row)">
              <el-icon><View /></el-icon>
              详情
            </el-button>
            
            <el-button type="text" size="small" @click="handleViewOrders(row)">
              <el-icon><Document /></el-icon>
              订单
            </el-button>
            
            <el-button type="text" size="small" @click="openEditDialog(row)">
              <el-icon><Edit /></el-icon>
              编辑
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
    
    <!-- 用户详情对话框 -->
    <el-dialog
      v-model="detailDialogVisible"
      title="用户详情"
      width="600px"
    >
      <div v-if="currentUser" class="user-detail">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="用户ID">{{ currentUser.id }}</el-descriptions-item>
          <el-descriptions-item label="姓名">{{ currentUser.name }}</el-descriptions-item>
          <el-descriptions-item label="手机号">{{ currentUser.phone }}</el-descriptions-item>
          <el-descriptions-item label="注册时间">{{ formatTime(currentUser.created_at) }}</el-descriptions-item>
          <el-descriptions-item label="地址" :span="2">{{ currentUser.address }}</el-descriptions-item>
          <el-descriptions-item label="总订单数">{{ currentUser.total_orders }}</el-descriptions-item>
          <el-descriptions-item label="进行中订单">{{ currentUser.active_orders }}</el-descriptions-item>
          <el-descriptions-item label="最后下单时间" :span="2">
            {{ currentUser.last_order_time ? formatTime(currentUser.last_order_time) : '无' }}
          </el-descriptions-item>
        </el-descriptions>
      </div>
    </el-dialog>
    
    <!-- 编辑用户对话框 -->
    <el-dialog v-model="editDialogVisible" title="编辑用户" width="600px">
      <el-form label-width="80px">
        <el-form-item label="姓名">
          <el-input v-model="editForm.name" placeholder="请输入姓名" />
        </el-form-item>
        <el-form-item label="手机号">
          <el-input v-model="editForm.phone" placeholder="请输入手机号" />
        </el-form-item>
        <el-form-item label="地址">
          <el-input v-model="editForm.address" placeholder="请输入地址" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="editDialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="savingEdit" @click="handleSaveEdit">保存</el-button>
      </template>
    </el-dialog>
    
    <!-- 用户订单对话框 -->
    <el-dialog
      v-model="ordersDialogVisible"
      :title="`${currentUser?.name} 的订单记录`"
      width="1000px"
    >
      <div class="user-orders">
        <!-- 订单搜索 -->
        <div class="orders-toolbar">
          <el-select
            v-model="orderSearchParams.status"
            placeholder="状态筛选"
            style="width: 120px;"
            clearable
            @change="getUserOrders"
          >
            <el-option label="待配送" value="待配送" />
            <el-option label="已配送" value="已配送" />
            <el-option label="使用中" value="使用中" />
            <el-option label="已归还" value="已归还" />
            <el-option label="已取消" value="已取消" />
          </el-select>
        </div>
        
        <!-- 订单表格 -->
        <el-table
          v-loading="ordersLoading"
          :data="userOrders"
          stripe
          style="width: 100%"
        >
          <el-table-column prop="order_no" label="订单号" width="180" />
          
          <el-table-column prop="wheelchair_name" label="轮椅" min-width="150" />
          
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
          
          <el-table-column label="操作" width="100">
            <template #default="{ row }">
              <el-button type="text" size="small" @click="handleViewOrderDetail(row)">
                <el-icon><View /></el-icon>
                详情
              </el-button>
            </template>
          </el-table-column>
        </el-table>
        
        <!-- 订单分页 -->
        <div class="pagination-container" style="margin-top: 16px;">
          <el-pagination
            v-model:current-page="orderSearchParams.page"
            v-model:page-size="orderSearchParams.limit"
            :total="ordersTotal"
            :page-sizes="[5, 10, 20]"
            layout="total, sizes, prev, pager, next"
            @size-change="handleOrderSizeChange"
            @current-change="handleOrderCurrentChange"
          />
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import {
  Search,
  Refresh,
  View,
  Document,
  User,
  Edit
} from '@element-plus/icons-vue'
import { userApi } from '@/api'
import type { User as UserType, Order, SearchParams } from '@/types/api'

// 响应式数据
const loading = ref(false)
const ordersLoading = ref(false)
const detailDialogVisible = ref(false)
const ordersDialogVisible = ref(false)
const tableData = ref<UserType[]>([])
const userOrders = ref<Order[]>([])
const currentUser = ref<UserType | null>(null)
const total = ref(0)
const ordersTotal = ref(0)

// 编辑对话框状态与表单
const editDialogVisible = ref(false)
const savingEdit = ref(false)
const editForm = reactive<{ name: string; phone: string; address: string }>({
  name: '',
  phone: '',
  address: ''
})

// 搜索参数
const searchParams = reactive<SearchParams>({
  page: 1,
  limit: 20,
  keyword: ''
})

// 订单搜索参数
const orderSearchParams = reactive<SearchParams>({
  page: 1,
  limit: 10,
  status: ''
})

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

// 获取用户列表
const getUserList = async () => {
  try {
    loading.value = true
    const response = await userApi.getList(searchParams)
    if (response.code === 200 && response.data) {
      // 适配后端 { list, total, page, limit, pages }
      const data: any = response.data
      tableData.value = (data.items ?? data.list ?? []).map((item: any) => ({
        id: item.id,
        name: item.name,
        phone: item.phone,
        address: item.address,
        total_orders: item.total_orders,
        active_orders: item.active_orders,
        created_at: item.created_at,
        last_order_time: item.last_order_time
      }))
      total.value = data.total ?? 0
      searchParams.page = data.page ?? searchParams.page
      searchParams.limit = data.limit ?? searchParams.limit
    } else {
      throw new Error(response.message || '获取用户列表失败')
    }
  } catch (error) {
    console.error('获取用户列表失败:', error)
    ElMessage.error('获取数据失败，请稍后重试')
  } finally {
    loading.value = false
  }
}

// 获取用户订单
const getUserOrders = async () => {
  if (!currentUser.value) return
  
  try {
    ordersLoading.value = true
    const response = await userApi.getUserOrders(currentUser.value.id, orderSearchParams)
    if (response.code === 200 && response.data) {
      const data: any = response.data
      const items = (data.items ?? data.list ?? [])
      userOrders.value = items
      ordersTotal.value = data.total ?? items.length
    } else {
      throw new Error(response.message || '获取订单数据失败')
    }
  } catch (error) {
    console.error('获取用户订单失败:', error)
    ElMessage.error('获取订单数据失败')
  } finally {
    ordersLoading.value = false
  }
}

// 搜索
const handleSearch = () => {
  searchParams.page = 1
  getUserList()
}

// 重置
const handleReset = () => {
  Object.assign(searchParams, {
    page: 1,
    limit: 20,
    keyword: ''
  })
  getUserList()
}

// 分页大小变化
const handleSizeChange = (size: number) => {
  searchParams.limit = size
  searchParams.page = 1
  getUserList()
}

// 当前页变化
const handleCurrentChange = (page: number) => {
  searchParams.page = page
  getUserList()
}

// 订单分页大小变化
const handleOrderSizeChange = (size: number) => {
  orderSearchParams.limit = size
  orderSearchParams.page = 1
  getUserOrders()
}

// 订单当前页变化
const handleOrderCurrentChange = (page: number) => {
  orderSearchParams.page = page
  getUserOrders()
}

// 查看用户详情
const handleViewDetail = async (row: UserType) => {
  try {
    // 模拟API调用获取详细信息
    // const response = await userApi.getDetail(row.id)
    // currentUser.value = response.data
    
    currentUser.value = row
    detailDialogVisible.value = true
  } catch (error) {
    console.error('获取用户详情失败:', error)
    ElMessage.error('获取用户详情失败')
  }
}

// 查看用户订单
const handleViewOrders = (row: UserType) => {
  currentUser.value = row
  orderSearchParams.page = 1
  orderSearchParams.status = ''
  ordersDialogVisible.value = true
  getUserOrders()
}

// 查看订单详情
const handleViewOrderDetail = (order: Order) => {
  ElMessage.info(`查看订单详情：${order.order_no}`)
  // 这里可以打开订单详情对话框或跳转到订单管理页面
}

// 组件挂载时获取数据
onMounted(() => {
  getUserList()
})
// 打开编辑对话框
const openEditDialog = (row: UserType) => {
  currentUser.value = row
  editForm.name = row.name || ''
  editForm.phone = row.phone || ''
  editForm.address = row.address || ''
  editDialogVisible.value = true
}

// 保存编辑
const handleSaveEdit = async () => {
  if (!currentUser.value) return
  try {
    savingEdit.value = true
    const res = await userApi.update(currentUser.value.id, {
      name: editForm.name,
      phone: editForm.phone,
      address: editForm.address
    })
    if (res.code === 200 && res.data) {
      const updated = res.data
      currentUser.value = {
        ...currentUser.value,
        name: updated.name,
        phone: updated.phone,
        address: updated.address,
        total_orders: updated.total_orders ?? currentUser.value.total_orders,
        active_orders: updated.active_orders ?? currentUser.value.active_orders,
        last_order_time: updated.last_order_time ?? currentUser.value.last_order_time
      }
      const idx = tableData.value.findIndex(u => u.id === currentUser.value!.id)
      if (idx !== -1) {
        tableData.value[idx] = { ...tableData.value[idx], ...currentUser.value }
      }
      ElMessage.success('保存成功')
      editDialogVisible.value = false
    } else {
      throw new Error(res.message || '更新失败')
    }
  } catch (e) {
    console.error('更新用户失败:', e)
    ElMessage.error('更新失败，请稍后重试')
  } finally {
    savingEdit.value = false
  }
}
</script>

<style scoped>
.user-management {
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
  display: flex;
  align-items: center;
  gap: 12px;
}

.user-avatar {
  flex-shrink: 0;
}

.user-details {
  flex: 1;
  min-width: 0;
}

.user-name {
  font-weight: 500;
  color: #2c3e50;
  margin-bottom: 4px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.user-phone {
  font-size: 12px;
  color: #7f8c8d;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.address-text {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 200px;
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

.user-detail {
  padding: 10px 0;
}

.user-orders {
  padding: 0;
}

.orders-toolbar {
  margin-bottom: 16px;
  display: flex;
  gap: 16px;
  align-items: center;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .search-form {
    justify-content: center;
  }
  
  .user-info {
    gap: 8px;
  }
  
  .user-avatar .el-avatar {
    width: 32px !important;
    height: 32px !important;
  }
}
</style>