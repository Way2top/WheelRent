<template>
  <div class="payment-container">
    <div class="content-wrapper">
      <el-card class="payment-card">
        <template #header>
          <div class="payment-header">
            <h2>确认支付</h2>
            <p>请确认订单信息并完成支付</p>
          </div>
        </template>
        
        <div v-if="wheelchair && preOrderId" class="payment-content">
          <!-- 订单信息 -->
          <div class="order-summary">
            <h3>订单信息</h3>
            
            <el-row :gutter="20">
              <el-col :xs="24" :md="8">
                <div class="wheelchair-image">
                  <img
                    :src="getWheelchairImage(wheelchair.id)"
                    :alt="wheelchair.name"
                    @error="handleImageError"
                  />
                </div>
              </el-col>
              
              <el-col :xs="24" :md="16">
                <div class="order-details">
                  <h4 class="wheelchair-name">{{ wheelchair.name }}</h4>
                  <p class="wheelchair-desc">{{ wheelchair.description }}</p>
                  
                  <div class="detail-row">
                    <span class="label">制造商：</span>
                    <span class="value">{{ wheelchair.manufacturer }}</span>
                  </div>
                  
                  <div class="detail-row">
                    <span class="label">租金：</span>
                    <span class="value price">¥{{ wheelchair.price }}/天</span>
                  </div>
                  
                  <div class="detail-row">
                    <span class="label">定金：</span>
                    <span class="value deposit">¥{{ wheelchair.price }}</span>
                  </div>
                </div>
              </el-col>
            </el-row>
          </div>
          
          <!-- 支付方式 -->
          <div class="payment-methods">
            <h3>支付方式</h3>
            
            <el-radio-group v-model="paymentMethod" size="large">
              <el-radio value="alipay" class="payment-option">
                <div class="payment-method-content">
                  <div class="payment-icon alipay">支</div>
                  <div class="payment-info">
                    <div class="method-name">支付宝</div>
                    <div class="method-desc">推荐使用支付宝快捷支付</div>
                  </div>
                </div>
              </el-radio>
              
              <el-radio value="wechat" class="payment-option">
                <div class="payment-method-content">
                  <div class="payment-icon wechat">微</div>
                  <div class="payment-info">
                    <div class="method-name">微信支付</div>
                    <div class="method-desc">使用微信扫码支付</div>
                  </div>
                </div>
              </el-radio>
              
              <el-radio value="bank" class="payment-option">
                <div class="payment-method-content">
                  <div class="payment-icon bank">银</div>
                  <div class="payment-info">
                    <div class="method-name">银行卡</div>
                    <div class="method-desc">使用储蓄卡或信用卡支付</div>
                  </div>
                </div>
              </el-radio>
            </el-radio-group>
          </div>
          
          <!-- 支付金额 -->
          <div class="payment-amount">
            <div class="amount-row">
              <span class="amount-label">应付金额：</span>
              <span class="amount-value">¥{{ wheelchair.price }}</span>
            </div>
          </div>
          
          <!-- 支付按钮 -->
          <div class="payment-actions">
            <el-button
              size="large"
              @click="goBack"
              style="width: 200px;"
            >
              返回修改
            </el-button>
            
            <el-button
              type="primary"
              size="large"
              style="width: 300px; height: 60px; font-size: 18px;"
              @click="confirmPayment"
              :loading="paying"
            >
              确认支付 ¥{{ wheelchair.price }}
            </el-button>
          </div>
          
          <!-- 倒计时提示 -->
          <div class="countdown-notice">
            <el-alert
              :title="`订单将在 ${countdown} 后过期，请尽快完成支付`"
              type="warning"
              :closable="false"
              show-icon
            />
          </div>
        </div>
        
        <div v-else class="loading-content">
          <el-skeleton :rows="8" animated />
        </div>
      </el-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { wheelchairApi, orderApi } from '@/api/wheelchair'
import type { Wheelchair } from '@/types/api'

const route = useRoute()
const router = useRouter()

// 响应式数据
const paying = ref(false)
const wheelchair = ref<Wheelchair | null>(null)
const preOrderId = ref('')
const paymentMethod = ref('alipay')
const countdown = ref('30:00')
const countdownTimer = ref<number | null>(null)
const remainingSeconds = ref(30 * 60) // 30分钟

// 获取轮椅图片
const getWheelchairImage = (id: number) => {
  return `https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=modern wheelchair medical equipment&image_size=square`
}

// 图片加载错误处理
const handleImageError = (event: Event) => {
  const img = event.target as HTMLImageElement
  img.src = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAwIiBoZWlnaHQ9IjIwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iMTAwJSIgaGVpZ2h0PSIxMDAlIiBmaWxsPSIjZGRkIi8+PHRleHQgeD0iNTAlIiB5PSI1MCUiIGZvbnQtZmFtaWx5PSJBcmlhbCIgZm9udC1zaXplPSIxNCIgZmlsbD0iIzk5OSIgdGV4dC1hbmNob3I9Im1pZGRsZSIgZHk9Ii4zZW0iPuWbvueJh+WKoOi9veWksei0pTwvdGV4dD48L3N2Zz4='
}

// 格式化倒计时
const formatCountdown = (seconds: number) => {
  const minutes = Math.floor(seconds / 60)
  const remainingSeconds = seconds % 60
  return `${minutes.toString().padStart(2, '0')}:${remainingSeconds.toString().padStart(2, '0')}`
}

// 开始倒计时
const startCountdown = () => {
  countdownTimer.value = window.setInterval(() => {
    remainingSeconds.value--
    countdown.value = formatCountdown(remainingSeconds.value)
    
    if (remainingSeconds.value <= 0) {
      clearInterval(countdownTimer.value!)
      ElMessage.error('订单已过期，请重新下单')
      router.push('/home')
    }
  }, 1000)
}

// 停止倒计时
const stopCountdown = () => {
  if (countdownTimer.value) {
    clearInterval(countdownTimer.value)
    countdownTimer.value = null
  }
}

// 获取轮椅详情
const getWheelchairDetail = async () => {
  try {
    const wheelchairId = Number(route.query.wheelchairId)
    preOrderId.value = route.query.preOrderId as string
    
    if (!wheelchairId || !preOrderId.value) {
      ElMessage.error('订单信息不完整')
      router.push('/home')
      return
    }
    
    const response = await wheelchairApi.getDetail(wheelchairId)
    
    if (response.code === 200 && response.data) {
      wheelchair.value = response.data
      startCountdown()
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

// 返回修改
const goBack = () => {
  router.go(-1)
}

// 确认支付
const confirmPayment = async () => {
  if (!preOrderId.value) {
    ElMessage.error('订单信息不完整')
    return
  }
  
  try {
    await ElMessageBox.confirm(
      '确认支付？支付成功后将生成正式订单。',
      '确认支付',
      {
        confirmButtonText: '确认支付',
        cancelButtonText: '取消',
        type: 'info'
      }
    )
    
    paying.value = true
    
    // 模拟支付过程
    await new Promise(resolve => setTimeout(resolve, 2000))
    
    // 提交正式订单
    const response = await orderApi.submitOrder({
      pre_order_id: preOrderId.value
    })
    
    if (response.code === 200 && response.data) {
      stopCountdown()
      
      // 跳转到成功页面
      router.push({
        name: 'OrderSuccess',
        query: {
          orderNo: response.data.order_no,
          orderId: response.data.order_id
        }
      })
    } else {
      ElMessage.error(response.message || '支付失败')
    }
  } catch (error: any) {
    if (error !== 'cancel') {
      console.error('支付失败:', error)
      ElMessage.error('支付失败，请稍后重试')
    }
  } finally {
    paying.value = false
  }
}

// 组件挂载时获取数据
onMounted(() => {
  getWheelchairDetail()
})

// 组件卸载时清理定时器
onUnmounted(() => {
  stopCountdown()
})
</script>

<style scoped>
.payment-container {
  min-height: calc(100vh - 200px);
  background-color: #f5f7fa;
}

.content-wrapper {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
}

.payment-card {
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.payment-header {
  text-align: center;
}

.payment-header h2 {
  margin: 0 0 0.5rem 0;
  font-size: 2rem;
  color: white;
}

.payment-header p {
  margin: 0;
  opacity: 0.9;
  font-size: 1.1rem;
}

.payment-card :deep(.el-card__header) {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  margin: -20px -20px 20px -20px;
  padding: 2rem;
}

.payment-content {
  padding: 1rem 0;
}

.order-summary {
  margin-bottom: 2rem;
  padding-bottom: 2rem;
  border-bottom: 1px solid #ebeef5;
}

.order-summary h3 {
  margin: 0 0 1.5rem 0;
  font-size: 1.3rem;
  color: #2c3e50;
}

.wheelchair-image {
  width: 100%;
  height: 200px;
  border-radius: 8px;
  overflow: hidden;
}

.wheelchair-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.order-details {
  padding-left: 1rem;
}

.wheelchair-name {
  margin: 0 0 0.5rem 0;
  font-size: 1.4rem;
  font-weight: 600;
  color: #2c3e50;
}

.wheelchair-desc {
  margin: 0 0 1rem 0;
  color: #7f8c8d;
  line-height: 1.4;
}

.detail-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
  padding: 0.5rem 0;
}

.detail-row .label {
  color: #7f8c8d;
  font-size: 1rem;
}

.detail-row .value {
  font-weight: 500;
  font-size: 1rem;
}

.detail-row .price {
  color: #e74c3c;
  font-size: 1.1rem;
}

.detail-row .deposit {
  color: #f39c12;
  font-size: 1.1rem;
}

.payment-methods {
  margin-bottom: 2rem;
  padding-bottom: 2rem;
  border-bottom: 1px solid #ebeef5;
}

.payment-methods h3 {
  margin: 0 0 1.5rem 0;
  font-size: 1.3rem;
  color: #2c3e50;
}

.payment-option {
  width: 100%;
  margin-bottom: 1rem;
  padding: 1rem;
  border: 2px solid #ebeef5;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.payment-option:hover {
  border-color: #409eff;
}

.payment-option.is-checked {
  border-color: #409eff;
  background-color: #f0f9ff;
}

.payment-method-content {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.payment-icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: bold;
  font-size: 1.2rem;
}

.payment-icon.alipay {
  background: #1677ff;
}

.payment-icon.wechat {
  background: #07c160;
}

.payment-icon.bank {
  background: #722ed1;
}

.payment-info {
  flex: 1;
}

.method-name {
  font-size: 1.1rem;
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 0.25rem;
}

.method-desc {
  font-size: 0.9rem;
  color: #7f8c8d;
}

.payment-amount {
  margin-bottom: 2rem;
  padding: 1.5rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 8px;
  color: white;
}

.amount-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.amount-label {
  font-size: 1.2rem;
}

.amount-value {
  font-size: 2rem;
  font-weight: 700;
}

.payment-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  gap: 1rem;
}

.countdown-notice {
  margin-top: 1rem;
}

.loading-content {
  padding: 2rem;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .content-wrapper {
    padding: 1rem;
  }
  
  .order-details {
    padding-left: 0;
    margin-top: 1rem;
  }
  
  .payment-actions {
    flex-direction: column;
  }
  
  .payment-actions .el-button {
    width: 100% !important;
  }
}
</style>