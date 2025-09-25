<template>
  <div class="wheelchair-detail-container">
    <div class="content-wrapper">
      <el-button 
        type="primary" 
        @click="goBack" 
        style="margin-bottom: 2rem"
      >
        <el-icon><ArrowLeft /></el-icon>
        返回列表
      </el-button>
      
      <el-card v-if="wheelchair" class="detail-card">
        <el-row :gutter="40">
          <el-col :xs="24" :md="12">
            <div class="wheelchair-image">
              <img
                :src="getWheelchairImage(wheelchair.id)"
                :alt="wheelchair.name"
                @error="handleImageError"
              />
            </div>
          </el-col>
          
          <el-col :xs="24" :md="12">
            <div class="wheelchair-info">
              <h1 class="wheelchair-title">{{ wheelchair.name }}</h1>
              
              <div class="wheelchair-meta">
                <el-tag type="info" size="large">
                  <el-icon><OfficeBuilding /></el-icon>
                  {{ wheelchair.manufacturer }}
                </el-tag>
                
                <el-tag 
                  :type="wheelchair.stock > 0 ? 'success' : 'danger'"
                  size="large"
                >
                  {{ wheelchair.stock > 0 ? `库存 ${wheelchair.stock}` : '暂无库存' }}
                </el-tag>
              </div>
              
              <div class="price-section">
                <div class="price">
                  <span class="price-label">租金：</span>
                  <span class="price-value">¥{{ wheelchair.price }}</span>
                  <span class="price-unit">/天</span>
                </div>
              </div>
              
              <div class="description-section">
                <h3>产品描述</h3>
                <p class="description">{{ wheelchair.description }}</p>
              </div>
              
              <div class="action-section">
                <el-button
                  type="primary"
                  size="large"
                  style="width: 100%; height: 60px; font-size: 18px;"
                  :disabled="wheelchair.stock <= 0"
                  @click="startRental"
                >
                  {{ wheelchair.stock > 0 ? '立即租赁' : '暂无库存' }}
                </el-button>
              </div>
            </div>
          </el-col>
        </el-row>
      </el-card>
      
      <el-card v-else-if="!loading" class="error-card">
        <el-empty description="轮椅信息不存在" />
      </el-card>
      
      <div v-if="loading" class="loading-container">
        <el-skeleton :rows="8" animated />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { ArrowLeft, OfficeBuilding } from '@element-plus/icons-vue'
import { wheelchairApi } from '@/api/wheelchair'
import type { Wheelchair } from '@/types/api'

const route = useRoute()
const router = useRouter()

// 响应式数据
const loading = ref(false)
const wheelchair = ref<Wheelchair | null>(null)

// 获取轮椅图片
const getWheelchairImage = (id: number) => {
  return `https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=modern wheelchair medical equipment detailed view&image_size=square`
}

// 图片加载错误处理
const handleImageError = (event: Event) => {
  const img = event.target as HTMLImageElement
  img.src = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAwIiBoZWlnaHQ9IjQwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iMTAwJSIgaGVpZ2h0PSIxMDAlIiBmaWxsPSIjZGRkIi8+PHRleHQgeD0iNTAlIiB5PSI1MCUiIGZvbnQtZmFtaWx5PSJBcmlhbCIgZm9udC1zaXplPSIxOCIgZmlsbD0iIzk5OSIgdGV4dC1hbmNob3I9Im1pZGRsZSIgZHk9Ii4zZW0iPuWbvueJh+WKoOi9veWksei0pTwvdGV4dD48L3N2Zz4='
}

// 获取轮椅详情
const getWheelchairDetail = async () => {
  try {
    loading.value = true
    const id = Number(route.params.id)
    
    if (!id || isNaN(id)) {
      ElMessage.error('无效的轮椅ID')
      router.push('/home')
      return
    }
    
    const response = await wheelchairApi.getDetail(id)
    
    if (response.code === 200 && response.data) {
      wheelchair.value = response.data
    } else {
      ElMessage.error(response.message || '获取轮椅详情失败')
      router.push('/home')
    }
  } catch (error) {
    console.error('获取轮椅详情失败:', error)
    ElMessage.error('获取轮椅详情失败，请稍后重试')
    router.push('/home')
  } finally {
    loading.value = false
  }
}

// 返回列表
const goBack = () => {
  router.push('/home')
}

// 开始租赁
const startRental = () => {
  if (!wheelchair.value) return
  
  router.push({
    name: 'OrderCreate',
    query: {
      wheelchairId: wheelchair.value.id
    }
  })
}

// 组件挂载时获取数据
onMounted(() => {
  getWheelchairDetail()
})
</script>

<style scoped>
.wheelchair-detail-container {
  min-height: calc(100vh - 200px);
  background-color: #f5f7fa;
}

.content-wrapper {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.detail-card {
  margin-bottom: 2rem;
}

.detail-card :deep(.el-card__body) {
  padding: 2rem;
}

.wheelchair-image {
  width: 100%;
  height: 400px;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.wheelchair-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.wheelchair-info {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.wheelchair-title {
  margin: 0 0 1.5rem 0;
  font-size: 2.5rem;
  font-weight: 600;
  color: #2c3e50;
  line-height: 1.2;
}

.wheelchair-meta {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
  flex-wrap: wrap;
}

.wheelchair-meta .el-tag {
  padding: 0.5rem 1rem;
  font-size: 1rem;
}

.price-section {
  margin-bottom: 2rem;
  padding: 1.5rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 12px;
  color: white;
}

.price {
  display: flex;
  align-items: baseline;
  gap: 0.5rem;
}

.price-label {
  font-size: 1.2rem;
  opacity: 0.9;
}

.price-value {
  font-size: 3rem;
  font-weight: 700;
}

.price-unit {
  font-size: 1.2rem;
  opacity: 0.9;
}

.description-section {
  margin-bottom: 2rem;
  flex: 1;
}

.description-section h3 {
  margin: 0 0 1rem 0;
  font-size: 1.5rem;
  color: #2c3e50;
}

.description {
  margin: 0;
  font-size: 1.1rem;
  line-height: 1.6;
  color: #5a6c7d;
}

.action-section {
  margin-top: auto;
}

.error-card {
  text-align: center;
  padding: 4rem 2rem;
}

.loading-container {
  padding: 2rem;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .content-wrapper {
    padding: 1rem;
  }
  
  .wheelchair-title {
    font-size: 2rem;
  }
  
  .price-value {
    font-size: 2.5rem;
  }
  
  .wheelchair-image {
    height: 300px;
    margin-bottom: 2rem;
  }
  
  .wheelchair-meta {
    justify-content: center;
  }
}
</style>