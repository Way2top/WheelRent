<template>
  <div class="wheelchair-management">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>轮椅管理</span>
          <el-button type="primary" @click="handleAdd">
            <el-icon><Plus /></el-icon>
            添加轮椅
          </el-button>
        </div>
      </template>
      
      <!-- 搜索工具栏 -->
      <div class="table-toolbar">
        <div class="search-form">
          <el-input
            v-model="searchParams.keyword"
            placeholder="搜索轮椅名称或制造商"
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
            <el-option label="可用" value="available" />
            <el-option label="维护中" value="maintenance" />
            <el-option label="已停用" value="discontinued" />
          </el-select>
          
          <el-button type="primary" @click="handleSearch">
            <el-icon><Search /></el-icon>
            搜索
          </el-button>
          
          <el-button @click="handleReset">
            <el-icon><Refresh /></el-icon>
            重置
          </el-button>
        </div>
        
        <div class="toolbar-actions">
          <el-button
            type="success"
            :disabled="!selectedRows.length"
            @click="handleBatchStatus('available')"
          >
            批量启用
          </el-button>
          
          <el-button
            type="warning"
            :disabled="!selectedRows.length"
            @click="handleBatchStatus('maintenance')"
          >
            批量维护
          </el-button>
        </div>
      </div>
      
      <!-- 数据表格 -->
      <el-table
        v-loading="loading"
        :data="tableData"
        @selection-change="handleSelectionChange"
        stripe
        style="width: 100%"
      >
        <el-table-column type="selection" width="55" />
        
        <el-table-column prop="id" label="ID" width="80" />
        
        <el-table-column prop="name" label="轮椅名称" min-width="150">
          <template #default="{ row }">
            <div class="wheelchair-info">
              <div class="wheelchair-image">
                <img
                  :src="getWheelchairImage(row.id)"
                  :alt="row.name"
                  @error="handleImageError"
                />
              </div>
              <div class="wheelchair-details">
                <div class="wheelchair-name">{{ row.name }}</div>
                <div class="wheelchair-desc">{{ row.description }}</div>
              </div>
            </div>
          </template>
        </el-table-column>
        
        <el-table-column prop="manufacturer" label="制造商" width="120" />
        
        <el-table-column prop="price" label="租金(元/天)" width="120">
          <template #default="{ row }">
            <span class="price">¥{{ row.price }}</span>
          </template>
        </el-table-column>
        
        <el-table-column prop="stock" label="库存" width="80">
          <template #default="{ row }">
            <el-tag
              :type="row.stock > 10 ? 'success' : row.stock > 0 ? 'warning' : 'danger'"
              size="small"
            >
              {{ row.stock }}
            </el-tag>
          </template>
        </el-table-column>
        
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag
              :type="getStatusType(row.status)"
              size="small"
            >
              {{ getStatusText(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        
        <el-table-column prop="created_at" label="创建时间" width="180">
          <template #default="{ row }">
            {{ formatTime(row.created_at) }}
          </template>
        </el-table-column>
        
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button type="text" size="small" @click="handleEdit(row)">
              <el-icon><Edit /></el-icon>
              编辑
            </el-button>
            
            <el-button type="text" size="small" @click="handleView(row)">
              <el-icon><View /></el-icon>
              查看
            </el-button>
            
            <el-button
              type="text"
              size="small"
              style="color: #f56c6c;"
              @click="handleDelete(row)"
            >
              <el-icon><Delete /></el-icon>
              删除
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
    
    <!-- 添加/编辑对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogTitle"
      width="600px"
      :before-close="handleDialogClose"
    >
      <el-form
        ref="formRef"
        :model="formData"
        :rules="formRules"
        label-width="100px"
      >
        <el-form-item label="轮椅名称" prop="name">
          <el-input v-model="formData.name" placeholder="请输入轮椅名称" />
        </el-form-item>
        
        <el-form-item label="描述" prop="description">
          <el-input
            v-model="formData.description"
            type="textarea"
            :rows="3"
            placeholder="请输入轮椅描述"
          />
        </el-form-item>
        
        <el-form-item label="制造商" prop="manufacturer">
          <el-input v-model="formData.manufacturer" placeholder="请输入制造商" />
        </el-form-item>
        
        <el-form-item label="租金" prop="price">
          <el-input-number
            v-model="formData.price"
            :min="0"
            :precision="2"
            placeholder="请输入每天租金"
            style="width: 100%;"
          />
        </el-form-item>
        
        <el-form-item label="库存" prop="stock">
          <el-input-number
            v-model="formData.stock"
            :min="0"
            placeholder="请输入库存数量"
            style="width: 100%;"
          />
        </el-form-item>
        
        <el-form-item label="状态" prop="status">
          <el-select v-model="formData.status" style="width: 100%;">
            <el-option label="可用" value="available" />
            <el-option label="维护中" value="maintenance" />
            <el-option label="已停用" value="discontinued" />
          </el-select>
        </el-form-item>
      </el-form>
      
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="submitLoading" @click="handleSubmit">
          确定
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed } from 'vue'
import { ElMessage, ElMessageBox, type FormInstance, type FormRules } from 'element-plus'
import {
  Plus,
  Search,
  Refresh,
  Edit,
  View,
  Delete
} from '@element-plus/icons-vue'
import { wheelchairApi } from '@/api'
import type { Wheelchair, WheelchairRequest, SearchParams } from '@/types/api'

// 响应式数据
const loading = ref(false)
const submitLoading = ref(false)
const dialogVisible = ref(false)
const formRef = ref<FormInstance>()
const tableData = ref<Wheelchair[]>([])
const selectedRows = ref<Wheelchair[]>([])
const total = ref(0)
const editingId = ref<number | null>(null)

// 搜索参数
const searchParams = reactive<SearchParams>({
  page: 1,
  limit: 20,
  keyword: '',
  status: ''
})

// 表单数据
const formData = reactive<WheelchairRequest>({
  name: '',
  description: '',
  manufacturer: '',
  price: 0,
  stock: 0,
  status: 'available'
})

// 表单验证规则
const formRules: FormRules = {
  name: [
    { required: true, message: '请输入轮椅名称', trigger: 'blur' },
    { min: 2, max: 50, message: '名称长度在 2 到 50 个字符', trigger: 'blur' }
  ],
  description: [
    { required: true, message: '请输入轮椅描述', trigger: 'blur' },
    { max: 200, message: '描述不能超过 200 个字符', trigger: 'blur' }
  ],
  manufacturer: [
    { required: true, message: '请输入制造商', trigger: 'blur' },
    { max: 50, message: '制造商名称不能超过 50 个字符', trigger: 'blur' }
  ],
  price: [
    { required: true, message: '请输入租金', trigger: 'blur' },
    { type: 'number', min: 0, message: '租金不能小于 0', trigger: 'blur' }
  ],
  stock: [
    { required: true, message: '请输入库存', trigger: 'blur' },
    { type: 'number', min: 0, message: '库存不能小于 0', trigger: 'blur' }
  ],
  status: [
    { required: true, message: '请选择状态', trigger: 'change' }
  ]
}

// 计算属性
const dialogTitle = computed(() => {
  return editingId.value ? '编辑轮椅' : '添加轮椅'
})

// 获取轮椅图片
const getWheelchairImage = (id: number) => {
  return `https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=modern wheelchair medical equipment&image_size=square`
}

// 图片加载错误处理
const handleImageError = (event: Event) => {
  const img = event.target as HTMLImageElement
  img.src = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjAiIGhlaWdodD0iNjAiIHZpZXdCb3g9IjAgMCA2MCA2MCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHJlY3Qgd2lkdGg9IjYwIiBoZWlnaHQ9IjYwIiBmaWxsPSIjRjVGN0ZBIi8+CjxwYXRoIGQ9Ik0yMCAyMEg0MFY0MEgyMFYyMFoiIGZpbGw9IiNEREREREQiLz4KPC9zdmc+'
}

// 获取状态类型
const getStatusType = (status: string) => {
  const typeMap: Record<string, string> = {
    available: 'success',
    maintenance: 'warning',
    discontinued: 'danger'
  }
  return typeMap[status] || 'info'
}

// 获取状态文本
const getStatusText = (status: string) => {
  const textMap: Record<string, string> = {
    available: '可用',
    maintenance: '维护中',
    discontinued: '已停用'
  }
  return textMap[status] || status
}

// 格式化时间
const formatTime = (timeStr: string) => {
  const date = new Date(timeStr)
  return date.toLocaleString('zh-CN')
}

// 获取轮椅列表
const getWheelchairList = async () => {
  try {
    loading.value = true
    
    // 模拟API调用
    // const response = await wheelchairApi.getList(searchParams)
    
    // 模拟数据
    const mockData = {
      items: [
        {
          id: 1,
          name: '标准轮椅 SW-001',
          description: '适合日常使用的标准轮椅，轻便舒适',
          manufacturer: '康复医疗',
          price: 50,
          stock: 15,
          status: 'available',
          created_at: '2024-01-01T10:00:00Z',
          updated_at: '2024-01-01T10:00:00Z'
        },
        {
          id: 2,
          name: '电动轮椅 EW-002',
          description: '电动助力轮椅，适合长距离使用',
          manufacturer: '智能医疗',
          price: 120,
          stock: 8,
          status: 'available',
          created_at: '2024-01-02T10:00:00Z',
          updated_at: '2024-01-02T10:00:00Z'
        },
        {
          id: 3,
          name: '轻便轮椅 LW-003',
          description: '超轻便折叠轮椅，方便携带',
          manufacturer: '便携医疗',
          price: 80,
          stock: 3,
          status: 'maintenance',
          created_at: '2024-01-03T10:00:00Z',
          updated_at: '2024-01-03T10:00:00Z'
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
    console.error('获取轮椅列表失败:', error)
    ElMessage.error('获取数据失败，请稍后重试')
  } finally {
    loading.value = false
  }
}

// 搜索
const handleSearch = () => {
  searchParams.page = 1
  getWheelchairList()
}

// 重置
const handleReset = () => {
  Object.assign(searchParams, {
    page: 1,
    limit: 20,
    keyword: '',
    status: ''
  })
  getWheelchairList()
}

// 选择变化
const handleSelectionChange = (selection: Wheelchair[]) => {
  selectedRows.value = selection
}

// 批量状态更新
const handleBatchStatus = async (status: string) => {
  try {
    const ids = selectedRows.value.map(row => row.id)
    
    await ElMessageBox.confirm(
      `确定要将选中的 ${ids.length} 个轮椅状态更新为"${getStatusText(status)}"吗？`,
      '批量操作确认',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    // 模拟API调用
    // await wheelchairApi.batchUpdateStatus(ids, status)
    
    ElMessage.success('批量更新成功')
    getWheelchairList()
  } catch (error: any) {
    if (error !== 'cancel') {
      console.error('批量更新失败:', error)
      ElMessage.error('批量更新失败，请稍后重试')
    }
  }
}

// 分页大小变化
const handleSizeChange = (size: number) => {
  searchParams.limit = size
  searchParams.page = 1
  getWheelchairList()
}

// 当前页变化
const handleCurrentChange = (page: number) => {
  searchParams.page = page
  getWheelchairList()
}

// 添加
const handleAdd = () => {
  editingId.value = null
  Object.assign(formData, {
    name: '',
    description: '',
    manufacturer: '',
    price: 0,
    stock: 0,
    status: 'available'
  })
  dialogVisible.value = true
}

// 编辑
const handleEdit = (row: Wheelchair) => {
  editingId.value = row.id
  Object.assign(formData, {
    name: row.name,
    description: row.description,
    manufacturer: row.manufacturer,
    price: row.price,
    stock: row.stock,
    status: row.status
  })
  dialogVisible.value = true
}

// 查看
const handleView = (row: Wheelchair) => {
  ElMessage.info(`查看轮椅详情：${row.name}`)
}

// 删除
const handleDelete = async (row: Wheelchair) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除轮椅"${row.name}"吗？此操作不可恢复。`,
      '删除确认',
      {
        confirmButtonText: '确定删除',
        cancelButtonText: '取消',
        type: 'error'
      }
    )
    
    // 模拟API调用
    // await wheelchairApi.delete(row.id)
    
    ElMessage.success('删除成功')
    getWheelchairList()
  } catch (error: any) {
    if (error !== 'cancel') {
      console.error('删除失败:', error)
      ElMessage.error('删除失败，请稍后重试')
    }
  }
}

// 提交表单
const handleSubmit = async () => {
  if (!formRef.value) return
  
  try {
    const valid = await formRef.value.validate()
    if (!valid) return
    
    submitLoading.value = true
    
    if (editingId.value)