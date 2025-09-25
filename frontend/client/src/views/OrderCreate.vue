<template>
  <div class="order-create-container">
    <div class="content-wrapper">
      <el-button 
        type="primary" 
        @click="goBack" 
        style="margin-bottom: 2rem"
      >
        <el-icon><ArrowLeft /></el-icon>
        返回详情
      </el-button>
      
      <el-row :gutter="40">
        <!-- 订单信息表单 -->
        <el-col :xs="24" :lg="14">
          <el-card class="form-card">
            <template #header>
              <h2>填写租赁信息</h2>
            </template>
            
            <el-form
              ref="formRef"
              :model="orderForm"
              :rules="formRules"
              label-width="100px"
              size="large"
            >
              <el-form-item label="姓名" prop="name">
                <el-input
                  v-model="orderForm.name"
                  placeholder="请输入您的姓名"
                  clearable
                />
              </el-form-item>
              
              <el-form-item label="手机号" prop="phone">
                <el-input
                  v-model="orderForm.phone"
                  placeholder="请输入手机号码"
                  clearable
                  maxlength="11"
                />
              </el-form-item>
              
              <el-form-item label="收货地址" prop="address">
                <el-input
                  v-model="orderForm.address"
                  type="textarea"
                  :rows="4"
                  placeholder="请输入详细的收货地址"
                  maxlength="200"
                  show-word-limit
                />
              </el-form-item>
              
              <el-form-item>
                <el-button
                  type="primary"
                  size="large"
                  style="width: 100%; height: 50px; font-size: 16px;"
                  @click="submitOrder"
                  :loading="submitting"
                >
                  确认租赁信息
                </el-button>
              </el-form-item>
            </el-form>
          </el-card>
        </el-col>
        
        <!-- 轮椅信息预览 -->
        <el-col :xs="24" :lg="10">
          <el-card class="preview-card">
            <template #header>
              <h3>租赁轮椅信息</h3>
            </template>
            
            <div v-if="wheelchair" class="wheelchair-preview">
              <div class="preview-image">
                <img
                  :src="getWheelchairImage(wheelchair.id)"
                  :alt="wheelchair.name"
                  @error="handleImageError"
                />
              </div>
              
              <div class="preview-info">
                <h4 class="wheelchair-name">{{ wheelchair.name }}</h4>
                <p class="wheelchair-desc">{{ wheelchair.description }}</p>
                
                <div class="wheelchair-details">
                  <div class="detail-item">
                    <span class="label">制造商：</span>
                    <span class="value">{{ wheelchair.manufacturer }}</span>
                  </div>
                  
                  <div class="detail-item">
                    <span class="label">库存：</span>
                    <el-tag 
                      :type="wheelchair.stock > 0 ? 'success' : 'danger'"
                      size="small"
                    >
                      {{ wheelchair.stock > 0 ? `${wheelchair.stock} 台` : '暂无库存' }}
                    </el-tag>
                  </div>
                </div>
                
                <div class="price-info">
                  <div class="price">
                    <span class="price-label">租金：</span>
                    <span class="price-value">¥{{ wheelchair.price }}</span>
                    <span class="price-unit">/天</span>
                  </div>
                  
                  <div class="deposit">
                    <span class="deposit-label">定金：</span>
                    <span class="deposit-value">¥{{ wheelchair.price }}</span>
                  </div>
                </div>
              </div>
            </div>
            
            <el-skeleton v-else :rows="6" animated />
          </el-card>
          
          <!-- 租赁须知 -->
          <el-card class="notice-card" style="margin-top: 1rem;">
            <template #header>
              <h4>租赁须知</h4>
            </template>
            
            <ul class="notice-list">
              <li>租赁期间请妥善保管轮椅，如有损坏需承担维修费用</li>
              <li>租赁费用按天计算，不足一天按一天计算</li>
              <li>定金在轮椅完好归还后全额退还</li>
              <li>如需延长租赁期，请提前联系客服</li>
              <li>轮椅配送范围仅限市区内，偏远地区需额外收费</li>
            </ul>
          </el-card>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox, type FormInstance, type FormRules } from 'element-plus'
import { ArrowLeft } from '@element-plus/icons-vue'
import { wheelchairApi, orderApi } from '@/api/wheelchair'
import type { Wheelchair } from '@/types/api'

const route = useRoute()
const router = useRouter()

// 响应式数据
const formRef = ref<FormInstance>()
const submitting = ref(false)
const wheelchair = ref<Wheelchair | null>(null)

// 表单数据
const orderForm = reactive({
  name: '',
  phone: '',
  address: ''
})

// 表单验证规则
const formRules: FormRules = {
  name: [
    { required: true, message: '请输入姓名', trigger: 'blur' },
    { min: 2, max: 20, message: '姓名长度在 2 到 20 个字符', trigger: 'blur' }
  ],
  phone: [
    { required: true, message: '请输入手机号码', trigger: 'blur' },
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号码', trigger: 'blur' }
  ],
  address: [
    { required: true, message: '请输入收货地址', trigger: 'blur' },
    { min: 10, max: 200, message: '地址长度在 10 到 200 个字符', trigger: 'blur' }
  ]
}

// 获取轮椅图片
const getWheelchairImage = (id: number) => {
  return `https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=modern wheelchair medical equipment&image_size=square`
}

// 图片加载错误处理
const handleImageError = (event: Event) => {
  const img = event.target as HTMLImageElement
  img.src = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAwIiBoZWlnaHQ9IjIwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iMTAwJSIgaGVpZ2h0PSIxMDAlIiBmaWxsPSIjZGRkIi8+PHRleHQgeD0iNTAlIiB5PSI1MCUiIGZvbnQtZmFtaWx5PSJBcmlhbCIgZm9udC1zaXplPSIxNCIgZmlsbD0iIzk5OSIgdGV4dC1hbmNob3I9Im1pZGRsZSIgZHk9Ii4zZW0iPuWbvueJh+WKoOi9veWksei0pTwvdGV4dD48L3N2Zz4='
}

// 获取轮椅详情
const getWheelchairDetail = async () => {
  try {
    const wheelchairId = Number(route.query.wheelchairId)
    
    if (!wheelchairId || isNaN(wheelchairId)) {
      ElMessage.error('无效的轮椅ID')
      router.push('/home')
      return
    }
    
    const response = await wheelchairApi.getDetail(wheelchairId)
    
    if (response.code === 200 && response.data) {
      wheelchair.value = response.data
      
      // 检查库存
      if (response.data.stock <= 0) {
        ElMessage.warning('该轮椅暂无库存')
        router.push('/home')
      }
    } else {
      ElMessage.error(response.message || '获取轮椅详情失败')
      router.push('/home')
    }
  } catch (error) {
    console.error('获取轮椅详情失败:', error)
    ElMessage.error('获取轮椅详情失败，请稍后重试')
    router.push('/home')
  }
}

// 返回详情页
const goBack = () => {
  if (wheelchair.value) {
    router.push(`/wheelchair/detail/${wheelchair.value.id}`)
  } else {
    router.push('/home')
  }
}

// 提交订单
const submitOrder = async () => {
  if (!formRef.value || !wheelchair.value) return
  
  try {
    // 表单验证
    await formRef.value.validate()
    
    // 确认对话框
    await ElMessageBox.confirm(
      `确认租赁 ${wheelchair.value.name}？\n定金：¥${wheelchair.value.price}`,
      '确认租赁',
      {
        confirmButtonText: '确认',
        cancelButtonText: '取消',
        type: 'info'
      }
    )
    
    submitting.value = true
    
    // 创建预订单
    const tempOrderResponse = await orderApi.createTempOrder({
      name: orderForm.name,
      phone: orderForm.phone,
      address: orderForm.address,
      wheelchair_id: wheelchair.value.id
    })
    
    if (tempOrderResponse.code === 200 && tempOrderResponse.data) {
      // 跳转到支付页面
      router.push({
        name: 'Payment',
        query: {
          preOrderId: tempOrderResponse.data.pre_order_id,
          wheelchairId: wheelchair.value.id
        }
      })
    } else {
      ElMessage.error(tempOrderResponse.message || '创建订单失败')
    }
  } catch (error: any) {
    if (error !== 'cancel') {
      console.error('提交订单失败:', error)
      ElMessage.error('提交订单失败，请稍后重试')
    }
  } finally {
    submitting.value = false
  }
}

// 组件挂载时获取数据
onMounted(() => {
  getWheelchairDetail()
})
</script>

<style scoped>
.order-create-container {
  min-height: calc(100vh - 200px);
  background-color: #f5f7fa;
}

.content-wrapper {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.form-card {
  height: fit-content;
}

.form-card :deep(.el-card__header) {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  margin: -20px -20px 20px -20px;
  padding: 1.5rem 2rem;
}

.form-card :deep(.el-card__header h2) {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 600;
}

.preview-card {
  position: sticky;
  top: 2rem;
}

.wheelchair-preview {
  text-align: center;
}

.preview-image {
  width: 100%;
  height: 200px;
  border-radius: 8px;
  overflow: hidden;
  margin-bottom: 1rem;
}

.preview-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.preview-info {
  text-align: left;
}

.wheelchair-name {
  margin: 0 0 0.5rem 0;
  font-size: 1.3rem;
  font-weight: 600;
  color: #2c3e50;
}

.wheelchair-desc {
  margin: 0 0 1rem 0;
  color: #7f8c8d;
  font-size: 0.9rem;
  line-height: 1.4;
}

.wheelchair-details {
  margin-bottom: 1.5rem;
}

.detail-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.detail-item .label {
  color: #7f8c8d;
  font-size: 0.9rem;
}

.detail-item .value {
  color: #2c3e50;
  font-weight: 500;
}

.price-info {
  padding: 1rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 8px;
  color: white;
}

.price {
  display: flex;
  align-items: baseline;
  gap: 0.25rem;
  margin-bottom: 0.5rem;
}

.price-label {
  font-size: 0.9rem;
  opacity: 0.9;
}

.price-value {
  font-size: 1.8rem;
  font-weight: 600;
}

.price-unit {
  font-size: 0.8rem;
  opacity: 0.9;
}

.deposit {
  display: flex;
  align-items: baseline;
  gap: 0.25rem;
  padding-top: 0.5rem;
  border-top: 1px solid rgba(255, 255, 255, 0.2);
}

.deposit-label {
  font-size: 0.9rem;
  opacity: 0.9;
}

.deposit-value {
  font-size: 1.2rem;
  font-weight: 600;
}

.notice-card :deep(.el-card__header) {
  padding: 1rem 1.5rem;
  background-color: #fdf6ec;
  border-bottom: 1px solid #faecd8;
}

.notice-card :deep(.el-card__header h4) {
  margin: 0;
  color: #e6a23c;
  font-size: 1rem;
}

.notice-list {
  margin: 0;
  padding-left: 1.2rem;
  color: #7f8c8d;
  font-size: 0.85rem;
  line-height: 1.6;
}

.notice-list li {
  margin-bottom: 0.5rem;
}

/* 响应式设计 */
@media (max-width: 992px) {
  .preview-card {
    position: static;
    margin-top: 2rem;
  }
}

@media (max-width: 768px) {
  .content-wrapper {
    padding: 1rem;
  }
}
</style>