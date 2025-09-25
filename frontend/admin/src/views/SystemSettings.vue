<template>
  <div class="system-settings">
    <el-row :gutter="20">
      <!-- 基本设置 -->
      <el-col :xs="24" :lg="12">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>基本设置</span>
              <el-button type="primary" :loading="basicLoading" @click="handleBasicSave">
                保存
              </el-button>
            </div>
          </template>
          
          <el-form
            ref="basicFormRef"
            :model="basicSettings"
            :rules="basicRules"
            label-width="120px"
          >
            <el-form-item label="网站名称" prop="site_name">
              <el-input
                v-model="basicSettings.site_name"
                placeholder="请输入网站名称"
              />
            </el-form-item>
            
            <el-form-item label="客服电话" prop="contact_phone">
              <el-input
                v-model="basicSettings.contact_phone"
                placeholder="请输入客服电话"
              />
            </el-form-item>
            
            <el-form-item label="客服邮箱" prop="contact_email">
              <el-input
                v-model="basicSettings.contact_email"
                placeholder="请输入客服邮箱"
              />
            </el-form-item>
            
            <el-form-item label="服务时间" prop="service_hours">
              <el-input
                v-model="basicSettings.service_hours"
                placeholder="例如：9:00-21:00"
              />
            </el-form-item>
            
            <el-form-item label="维护模式">
              <el-switch
                v-model="basicSettings.maintenance_mode"
                active-text="开启"
                inactive-text="关闭"
              />
              <div class="form-tip">
                开启后，客户端将显示维护页面
              </div>
            </el-form-item>
          </el-form>
        </el-card>
      </el-col>
      
      <!-- 业务设置 -->
      <el-col :xs="24" :lg="12">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>业务设置</span>
              <el-button type="primary" :loading="businessLoading" @click="handleBusinessSave">
                保存
              </el-button>
            </div>
          </template>
          
          <el-form
            ref="businessFormRef"
            :model="businessSettings"
            :rules="businessRules"
            label-width="120px"
          >
            <el-form-item label="配送费用" prop="delivery_fee">
              <el-input-number
                v-model="businessSettings.delivery_fee"
                :min="0"
                :precision="2"
                placeholder="请输入配送费用"
                style="width: 100%;"
              />
              <div class="form-tip">
                单位：元，0表示免费配送
              </div>
            </el-form-item>
            
            <el-form-item label="最大租赁天数" prop="max_rental_days">
              <el-input-number
                v-model="businessSettings.max_rental_days"
                :min="1"
                :max="365"
                placeholder="请输入最大租赁天数"
                style="width: 100%;"
              />
              <div class="form-tip">
                单位：天，限制单次租赁的最大天数
              </div>
            </el-form-item>
            
            <el-form-item label="定金比例" prop="deposit_rate">
              <el-input-number
                v-model="businessSettings.deposit_rate"
                :min="0"
                :max="100"
                :precision="2"
                placeholder="请输入定金比例"
                style="width: 100%;"
              />
              <div class="form-tip">
                单位：%，定金 = 租金 × 定金比例
              </div>
            </el-form-item>
          </el-form>
        </el-card>
      </el-col>
    </el-row>
    
    <!-- 系统信息 -->
    <el-row :gutter="20" style="margin-top: 20px;">
      <el-col :span="24">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>系统信息</span>
              <el-button type="primary" @click="handleRefreshInfo">
                <el-icon><Refresh /></el-icon>
                刷新
              </el-button>
            </div>
          </template>
          
          <el-row :gutter="20">
            <el-col :xs="24" :sm="12" :lg="6">
              <div class="info-card">
                <div class="info-icon system">
                  <el-icon size="32"><Monitor /></el-icon>
                </div>
                <div class="info-content">
                  <div class="info-title">系统版本</div>
                  <div class="info-value">v1.0.0</div>
                </div>
              </div>
            </el-col>
            
            <el-col :xs="24" :sm="12" :lg="6">
              <div class="info-card">
                <div class="info-icon database">
                  <el-icon size="32"><Coin /></el-icon>
                </div>
                <div class="info-content">
                  <div class="info-title">数据库</div>
                  <div class="info-value">SQLite</div>
                </div>
              </div>
            </el-col>
            
            <el-col :xs="24" :sm="12" :lg="6">
              <div class="info-card">
                <div class="info-icon runtime">
                  <div class="info-content">
                    <div class="info-title">运行时间</div>
                    <div class="info-value">{{ systemUptime }}</div>
                  </div>
                </div>
              </div>
            </el-col>
            
            <el-col :xs="24" :sm="12" :lg="6">
              <div class="info-card">
                <div class="info-icon status">
                  <el-icon size="32"><CircleCheck /></el-icon>
                </div>
                <div class="info-content">
                  <div class="info-title">系统状态</div>
                  <div class="info-value status-normal">正常</div>
                </div>
              </div>
            </el-col>
          </el-row>
        </el-card>
      </el-col>
    </el-row>
    
    <!-- 操作日志 -->
    <el-row :gutter="20" style="margin-top: 20px;">
      <el-col :span="24">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>最近操作日志</span>
              <el-button type="text" @click="handleViewAllLogs">
                查看全部
              </el-button>
            </div>
          </template>
          
          <el-timeline>
            <el-timeline-item
              v-for="(log, index) in operationLogs"
              :key="index"
              :timestamp="log.time"
              :type="log.type"
            >
              <div class="log-content">
                <div class="log-title">{{ log.title }}</div>
                <div class="log-desc">{{ log.description }}</div>
                <div class="log-user">操作人：{{ log.user }}</div>
              </div>
            </el-timeline-item>
          </el-timeline>
          
          <div v-if="operationLogs.length === 0" class="empty-logs">
            <el-empty description="暂无操作记录" :image-size="80" />
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed } from 'vue'
import { ElMessage, type FormInstance, type FormRules } from 'element-plus'
import {
  Refresh,
  Monitor,
  Coin,
  CircleCheck
} from '@element-plus/icons-vue'
import { settingsApi } from '@/api'
import type { SystemSettings } from '@/types/api'

// 响应式数据
const basicLoading = ref(false)
const businessLoading = ref(false)
const basicFormRef = ref<FormInstance>()
const businessFormRef = ref<FormInstance>()
const systemStartTime = ref(new Date())

// 基本设置
const basicSettings = reactive({
  site_name: '在线轮椅租赁系统',
  contact_phone: '400-888-8888',
  contact_email: 'service@wheelchair-rental.com',
  service_hours: '9:00-21:00',
  maintenance_mode: false
})

// 业务设置
const businessSettings = reactive({
  delivery_fee: 0,
  max_rental_days: 30,
  deposit_rate: 100
})

// 操作日志
const operationLogs = ref([
  {
    time: '2024-01-15 14:30',
    type: 'primary',
    title: '系统设置更新',
    description: '更新了客服电话和服务时间',
    user: 'admin'
  },
  {
    time: '2024-01-15 13:45',
    type: 'success',
    title: '轮椅信息更新',
    description: '更新了标准轮椅 SW-001 的库存信息',
    user: 'admin'
  },
  {
    time: '2024-01-15 12:20',
    type: 'warning',
    title: '订单状态变更',
    description: '订单 #WR20240115001 状态更新为已配送',
    user: 'admin'
  },
  {
    time: '2024-01-15 11:15',
    type: 'info',
    title: '用户数据导出',
    description: '导出了用户订单数据报表',
    user: 'admin'
  }
])

// 表单验证规则
const basicRules: FormRules = {
  site_name: [
    { required: true, message: '请输入网站名称', trigger: 'blur' },
    { min: 2, max: 50, message: '网站名称长度在 2 到 50 个字符', trigger: 'blur' }
  ],
  contact_phone: [
    { required: true, message: '请输入客服电话', trigger: 'blur' },
    { pattern: /^[0-9-+()\s]+$/, message: '请输入正确的电话号码', trigger: 'blur' }
  ],
  contact_email: [
    { required: true, message: '请输入客服邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
  ],
  service_hours: [
    { required: true, message: '请输入服务时间', trigger: 'blur' }
  ]
}

const businessRules: FormRules = {
  delivery_fee: [
    { required: true, message: '请输入配送费用', trigger: 'blur' },
    { type: 'number', min: 0, message: '配送费用不能小于 0', trigger: 'blur' }
  ],
  max_rental_days: [
    { required: true, message: '请输入最大租赁天数', trigger: 'blur' },
    { type: 'number', min: 1, max: 365, message: '租赁天数在 1 到 365 天之间', trigger: 'blur' }
  ],
  deposit_rate: [
    { required: true, message: '请输入定金比例', trigger: 'blur' },
    { type: 'number', min: 0, max: 100, message: '定金比例在 0 到 100 之间', trigger: 'blur' }
  ]
}

// 计算系统运行时间
const systemUptime = computed(() => {
  const now = new Date()
  const diff = now.getTime() - systemStartTime.value.getTime()
  const days = Math.floor(diff / (1000 * 60 * 60 * 24))
  const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60))
  const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60))
  
  if (days > 0) {
    return `${days}天${hours}小时${minutes}分钟`
  } else if (hours > 0) {
    return `${hours}小时${minutes}分钟`
  } else {
    return `${minutes}分钟`
  }
})

// 获取系统设置
const getSystemSettings = async () => {
  try {
    // 模拟API调用
    // const response = await settingsApi.getSettings()
    
    // 模拟数据已在reactive中初始化
    ElMessage.success('设置加载完成')
  } catch (error) {
    console.error('获取系统设置失败:', error)
    ElMessage.error('获取设置失败，请稍后重试')
  }
}

// 保存基本设置
const handleBasicSave = async () => {
  if (!basicFormRef.value) return
  
  try {
    const valid = await basicFormRef.value.validate()
    if (!valid) return
    
    basicLoading.value = true
    
    // 模拟API调用
    // await settingsApi.updateSettings(basicSettings)
    
    ElMessage.success('基本设置保存成功')
  } catch (error) {
    console.error('保存基本设置失败:', error)
    ElMessage.error('保存失败，请稍后重试')
  } finally {
    basicLoading.value = false
  }
}

// 保存业务设置
const handleBusinessSave = async () => {
  if (!businessFormRef.value) return
  
  try {
    const valid = await businessFormRef.value.validate()
    if (!valid) return
    
    businessLoading.value = true
    
    // 模拟API调用
    // await settingsApi.updateSettings(businessSettings)
    
    ElMessage.success('业务设置保存成功')
  } catch (error) {
    console.error('保存业务设置失败:', error)
    ElMessage.error('保存失败，请稍后重试')
  } finally {
    businessLoading.value = false
  }
}

// 刷新系统信息
const handleRefreshInfo = () => {
  systemStartTime.value = new Date(Date.now() - Math.random() * 1000 * 60 * 60 * 24 * 7) // 模拟7天内的随机启动时间
  ElMessage.success('系统信息已刷新')
}

// 查看全部日志
const handleViewAllLogs = () => {
  ElMessage.info('查看全部日志功能开发中...')
}

// 组件挂载时获取数据
onMounted(() => {
  getSystemSettings()
  // 设置一个随机的系统启动时间（模拟）
  systemStartTime.value = new Date(Date.now() - Math.random() * 1000 * 60 * 60 * 24 * 7)
})
</script>

<style scoped>
.system-settings {
  padding: 0;
}

.form-tip {
  font-size: 12px;
  color: #909399;
  margin-top: 4px;
  line-height: 1.4;
}

.info-card {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px;
  background-color: #f8f9fa;
  border-radius: 8px;
  margin-bottom: 16px;
  transition: all 0.3s;
}

.info-card:hover {
  background-color: #e9ecef;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.info-icon {
  width: 60px;
  height: 60px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  flex-shrink: 0;
}

.info-icon.system {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.info-icon.database {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
}

.info-icon.runtime {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
}

.info-icon.status {
  background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
}

.info-content {
  flex: 1;
}

.info-title {
  font-size: 14px;
  color: #7f8c8d;
  margin-bottom: 4px;
}

.info-value {
  font-size: 18px;
  font-weight: 600;
  color: #2c3e50;
}

.info-value.status-normal {
  color: #67c23a;
}

.log-content {
  padding-left: 10px;
}

.log-title {
  font-size: 14px;
  font-weight: 500;
  color: #2c3e50;
  margin-bottom: 4px;
}

.log-desc {
  font-size: 12px;
  color: #7f8c8d;
  line-height: 1.4;
  margin-bottom: 4px;
}

.log-user {
  font-size: 11px;
  color: #bdc3c7;
}

.empty-logs {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 200px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .info-card {
    gap: 12px;
    padding: 16px;
  }
  
  .info-icon {
    width: 48px;
    height: 48px;
  }
  
  .info-icon .el-icon {
    font-size: 24px !important;
  }
  
  .info-value {
    font-size: 16px;
  }
}
</style>