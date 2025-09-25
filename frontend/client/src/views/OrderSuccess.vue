<template>
  <div class="order-success-container">
    <div class="content-wrapper">
      <el-card class="success-card">
        <!-- 成功图标和标题 -->
        <div class="success-header">
          <div class="success-icon">
            <el-icon size="80" color="#67C23A">
              <CircleCheck />
            </el-icon>
          </div>
          
          <h1 class="success-title">支付成功！</h1>
          <p class="success-subtitle">您的轮椅租赁订单已生成，我们将尽快为您配送</p>
        </div>
        
        <!-- 订单信息 -->
        <div v-if="orderInfo" class="order-info">
          <h3>订单详情</h3>
          
          <div class="info-grid">
            <div class="info-item">
              <span class="label">订单号：</span>
              <span class="value order-no">{{ orderInfo.order_no }}</span>
              <el-button 
                type="text" 
                size="small" 
                @click="copyOrderNo"
              >
                复制
              </el-button>
            </div>
            
            <div class="info-item">
              <span class="label">轮椅名称：</span>
              <span class="value">{{ orderInfo.wheelchair_name }}</span>
            </div>
            
            <div class="info-item">
              <span class="label">租赁人：</span>
              <span class="value">{{ orderInfo.user_name }}</span>
            </div>
            
            <div class="info-item">
              <span class="label">联系电话：</span>
              <span class="value">{{ orderInfo.user_phone }}</span>
            </div>
            
            <div class="info-item">
              <span class="label">配送地址：</span>
              <span class="value">{{ orderInfo.user_address }}</span>
            </div>
            
            <div class="info-item">
              <span class="label">定金金额：</span>
              <span class="value price">¥{{ orderInfo.deposit }}</span>
            </div>
            
            <div class="info-item">
              <span class="label">订单状态：</span>
              <el-tag type="warning" size="large">{{ orderInfo.status }}</el-tag>
            </div>
            
            <div class="info-item">
              <span class="label">下单时间：</span>
              <span class="value">{{ formatTime(orderInfo.create_time) }}</span>
            </div>
          </div>
        </div>
        
        <!-- 配送信息 -->
        <div class="delivery-info">
          <h3>配送信息</h3>
          
          <el-timeline>
            <el-timeline-item
              timestamp="预计2小时内"
              type="primary"
              size="large"
            >
              <h4>订单确认</h4>
              <p>我们已收到您的订单，正在安排配送人员</p>
            </el-timeline-item>
            
            <el-timeline-item
              timestamp="预计4-6小时"
              type="info"
              size="large"
            >
              <h4>准备配送</h4>
              <p>轮椅已准备完毕，配送人员即将出发</p>
            </el-timeline-item>
            
            <el-timeline-item
              timestamp="预计当日送达"
              type="success"
              size="large"
            >
              <h4>送达完成</h4>
              <p>轮椅送达指定地址，请验收并开始使用</p>
            </el-timeline-item>
          </el-timeline>
        </div>
        
        <!-- 温馨提示 -->
        <div class="tips-section">
          <h3>温馨提示</h3>
          
          <el-alert
            title="重要提醒"
            type="info"
            :closable="false"
            show-icon
          >
            <ul class="tips-list">
              <li>配送人员会在送达前30分钟电话联系您</li>
              <li>请保持手机畅通，确保能及时接收配送信息</li>
              <li>收到轮椅后请仔细检查，如有问题请及时联系客服</li>
              <li>定金将在轮椅完好归还后全额退还</li>
              <li>如需延长租赁期，请提前3天联系客服</li>
            </ul>
          </el-alert>
        </div>
        
        <!-- 联系方式 -->
        <div class="contact-section">
          <h3>联系我们</h3>
          
          <el-row :gutter="20">
            <el-col :xs="24" :sm="8">
              <div class="contact-item">
                <el-icon size="24" color="#409EFF"><Phone /></el-icon>
                <div class="contact-info">
                  <div class="contact-label">客服热线</div>
                  <div class="contact-value">400-888-8888</div>
                </div>
              </div>
            </el-col>
            
            <el-col :xs="24" :sm="8">
              <div class="contact-item">
                <el-icon size="24" color="#67C23A"><Message /></el-icon>
                <div class="contact-info">
                  <div class="contact-label">在线客服</div>
                  <div class="contact-value">9:00-21:00</div>
                </div>
              </div>
            </el-col>
            
            <el-col :xs="24" :sm="8">
              <div class="contact-item">
                <el-icon size="24" color="#E6A23C"><Clock /></el-icon>
                <div class="contact-info">
                  <div class="contact-label">服务时间</div>
                  <div class="contact-value">24小时</div>
                </div>
              </div>
            </el-col>
          </el-row>
        </div>
        
        <!-- 操作按钮 -->
        <div class="action-buttons">
          <el-button
            size="large"
            @click="goHome"
            style="width: 200px;"
          >
            返回首页
          </el-button>
          
          <el-button
            type="primary"
            size="large"
            @click="viewOrder"
            style="width: 200px;"
          >
            查看订单
          </el-button>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { CircleCheck, Phone, Message, Clock } from '@element-plus/icons-vue'
import { orderApi } from '@/api/wheelchair'
import type { Order } from '@/types/api'

const route = useRoute()
const router = useRouter()

// 响应式数据
const orderInfo = ref<Order | null>(null)

// 格式化时间
const formatTime = (timeStr: string) => {
  const date = new Date(timeStr)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  })
}

// 复制订单号
const copyOrderNo = async () => {
  if (!orderInfo.value) return
  
  try {
    await navigator.clipboard.writeText(orderInfo.value.order_no)
    ElMessage.success('订单号已复制到剪贴板')
  } catch (error) {
    // 降级方案
    const textArea = document.createElement('textarea')
    textArea.value = orderInfo.value.order_no
    document.body.appendChild(textArea)
    textArea.select()
    document.execCommand('copy')
    document.body.removeChild(textArea)
    ElMessage.success('订单号已复制到剪贴板')
  }
}

// 获取订单详情
const getOrderDetail = async () => {
  try {
    const orderNo = route.query.orderNo as string
    
    if (!orderNo) {
      ElMessage.error('订单号不存在')
      router.push('/home')
      return
    }
    
    const response = await orderApi.getOrderDetail(orderNo)
    
    if (response.code === 200 && response.data) {
      orderInfo.value = response.data
    } else {
      ElMessage.error(response.message || '获取订单详情失败')
      // 如果获取失败，使用路由参数中的基本信息
      const orderId = route.query.orderId as string
      if (orderId) {
        orderInfo.value = {
          id: Number(orderId),
          order_no: orderNo,
          user_name: '用户',
          user_phone: '',
          user_address: '',
          wheelchair_id: 0,
          wheelchair_name: '轮椅',
          deposit: 0,
          status: '待配送',
          create_time: new Date().toISOString()
        }
      }
    }
  } catch (error) {
    console.error('获取订单详情失败:', error)
    ElMessage.error('获取订单详情失败，请稍后重试')
  }
}

// 返回首页
const goHome = () => {
  router.push('/home')
}

// 查看订单（这里可以跳转到订单详情页，暂时显示提示）
const viewOrder = () => {
  if (orderInfo.value) {
    ElMessage.info(`订单号：${orderInfo.value.order_no}，您可以保存此订单号以便后续查询`)
  }
}

// 组件挂载时获取数据
onMounted(() => {
  getOrderDetail()
})
</script>

<style scoped>
.order-success-container {
  min-height: calc(100vh - 200px);
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 2rem 0;
}

.content-wrapper {
  max-width: 800px;
  margin: 0 auto;
  padding: 0 2rem;
}

.success-card {
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.success-header {
  text-align: center;
  padding: 2rem 0;
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  color: white;
  margin: -20px -20px 2rem -20px;
}

.success-icon {
  margin-bottom: 1rem;
}

.success-title {
  margin: 0 0 0.5rem 0;
  font-size: 2.5rem;
  font-weight: 600;
}

.success-subtitle {
  margin: 0;
  font-size: 1.2rem;
  opacity: 0.9;
}

.order-info {
  margin-bottom: 2rem;
  padding-bottom: 2rem;
  border-bottom: 1px solid #ebeef5;
}

.order-info h3 {
  margin: 0 0 1.5rem 0;
  font-size: 1.4rem;
  color: #2c3e50;
}

.info-grid {
  display: grid;
  gap: 1rem;
}

.info-item {
  display: flex;
  align-items: center;
  padding: 0.75rem 0;
  border-bottom: 1px solid #f5f7fa;
}

.info-item .label {
  width: 120px;
  color: #7f8c8d;
  font-weight: 500;
  flex-shrink: 0;
}

.info-item .value {
  flex: 1;
  color: #2c3e50;
  font-weight: 500;
}

.info-item .order-no {
  font-family: 'Courier New', monospace;
  font-size: 1.1rem;
  color: #409eff;
  font-weight: 600;
}

.info-item .price {
  color: #e74c3c;
  font-size: 1.2rem;
  font-weight: 600;
}

.delivery-info {
  margin-bottom: 2rem;
  padding-bottom: 2rem;
  border-bottom: 1px solid #ebeef5;
}

.delivery-info h3 {
  margin: 0 0 1.5rem 0;
  font-size: 1.4rem;
  color: #2c3e50;
}

.delivery-info :deep(.el-timeline-item__content) {
  padding-bottom: 1.5rem;
}

.delivery-info h4 {
  margin: 0 0 0.5rem 0;
  font-size: 1.1rem;
  color: #2c3e50;
}

.delivery-info p {
  margin: 0;
  color: #7f8c8d;
  line-height: 1.4;
}

.tips-section {
  margin-bottom: 2rem;
  padding-bottom: 2rem;
  border-bottom: 1px solid #ebeef5;
}

.tips-section h3 {
  margin: 0 0 1.5rem 0;
  font-size: 1.4rem;
  color: #2c3e50;
}

.tips-list {
  margin: 1rem 0 0 0;
  padding-left: 1.2rem;
  color: #5a6c7d;
  line-height: 1.6;
}

.tips-list li {
  margin-bottom: 0.5rem;
}

.contact-section {
  margin-bottom: 2rem;
}

.contact-section h3 {
  margin: 0 0 1.5rem 0;
  font-size: 1.4rem;
  color: #2c3e50;
}

.contact-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background-color: #f8f9fa;
  border-radius: 8px;
  margin-bottom: 1rem;
}

.contact-info {
  flex: 1;
}

.contact-label {
  font-size: 0.9rem;
  color: #7f8c8d;
  margin-bottom: 0.25rem;
}

.contact-value {
  font-size: 1.1rem;
  font-weight: 600;
  color: #2c3e50;
}

.action-buttons {
  display: flex;
  justify-content: center;
  gap: 2rem;
  padding-top: 2rem;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .content-wrapper {
    padding: 0 1rem;
  }
  
  .success-title {
    font-size: 2rem;
  }
  
  .success-subtitle {
    font-size: 1rem;
  }
  
  .info-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }
  
  .info-item .label {
    width: auto;
  }
  
  .action-buttons {
    flex-direction: column;
    align-items: center;
  }
  
  .action-buttons .el-button {
    width: 100% !important;
    max-width: 300px;
  }
}
</style>