<template>
  <div class="home-container">
    <div class="content-wrapper">
      <!-- 搜索区域 -->
      <div class="search-section">
        <el-card class="search-card">
          <div class="search-header">
            <h2>轮椅租赁服务</h2>
            <p>为失能老人提供专业的轮椅租赁服务</p>
          </div>
          
          <div class="search-form">
            <el-row :gutter="20" align="middle">
              <el-col :span="12">
                <el-input
                  v-model="searchKeyword"
                  placeholder="请输入轮椅名称或制造商"
                  size="large"
                  clearable
                  @keyup.enter="handleSearch"
                >
                  <template #prefix>
                    <el-icon><Search /></el-icon>
                  </template>
                </el-input>
              </el-col>
              <el-col :span="6">
                <el-select
                  v-model="sortType"
                  placeholder="排序方式"
                  size="large"
                  style="width: 100%"
                >
                  <el-option label="默认排序" value="" />
                  <el-option label="价格从低到高" value="price_asc" />
                  <el-option label="价格从高到低" value="price_desc" />
                </el-select>
              </el-col>
              <el-col :span="6">
                <el-button
                  type="primary"
                  size="large"
                  style="width: 100%"
                  @click="handleSearch"
                  :loading="loading"
                >
                  搜索轮椅
                </el-button>
              </el-col>
            </el-row>
          </div>
        </el-card>
      </div>

      <!-- 轮椅列表 -->
      <div class="wheelchair-list">
        <el-row :gutter="20">
          <el-col
            v-for="wheelchair in wheelchairs"
            :key="wheelchair.id"
            :xs="24"
            :sm="12"
            :md="8"
            :lg="6"
            style="margin-bottom: 20px"
          >
            <el-card class="wheelchair-card" shadow="hover">
              <div class="wheelchair-image">
                <img
                  :src="getWheelchairImage(wheelchair.id)"
                  :alt="wheelchair.name"
                  @error="handleImageError"
                />
              </div>
              
              <div class="wheelchair-info">
                <h3 class="wheelchair-name">{{ wheelchair.name }}</h3>
                <p class="wheelchair-desc">{{ wheelchair.description }}</p>
                <p class="wheelchair-manufacturer">
                  <el-icon><OfficeBuilding /></el-icon>
                  {{ wheelchair.manufacturer }}
                </p>
                
                <div class="wheelchair-details">
                  <div class="price">
                    <span class="price-label">租金：</span>
                    <span class="price-value">¥{{ wheelchair.price }}</span>
                    <span class="price-unit">/天</span>
                  </div>
                  
                  <div class="stock">
                    <el-tag
                      :type="wheelchair.stock > 0 ? 'success' : 'danger'"
                      size="small"
                    >
                      {{ wheelchair.stock > 0 ? `库存 ${wheelchair.stock}` : '暂无库存' }}
                    </el-tag>
                  </div>
                </div>
                
                <div class="wheelchair-actions">
                  <el-button
                    type="primary"
                    size="large"
                    style="width: 100%"
                    :disabled="wheelchair.stock <= 0"
                    @click="viewDetail(wheelchair.id)"
                  >
                    {{ wheelchair.stock > 0 ? '立即租赁' : '暂无库存' }}
                  </el-button>
                </div>
              </div>
            </el-card>
          </el-col>
        </el-row>
        
        <!-- 空状态 -->
        <el-empty
          v-if="!loading && wheelchairs.length === 0"
          description="暂无轮椅信息"
          :image-size="200"
        />
        
        <!-- 分页 -->
        <div v-if="total > 0" class="pagination">
          <el-pagination
            v-model:current-page="currentPage"
            v-model:page-size="pageSize"
            :page-sizes="[8, 16, 24, 32]"
            :total="total"
            layout="total, sizes, prev, pager, next, jumper"
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Search, OfficeBuilding } from '@element-plus/icons-vue'
import { wheelchairApi } from '@/api/wheelchair'
import type { Wheelchair } from '@/types/api'

const router = useRouter()

// 响应式数据
const loading = ref(false)
const searchKeyword = ref('')
const sortType = ref('')
const wheelchairs = ref<Wheelchair[]>([])
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(8)

// 获取轮椅图片
const getWheelchairImage = (id: number) => {
  return `https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=modern wheelchair medical equipment clean background&image_size=square`
}

// 图片加载错误处理
const handleImageError = (event: Event) => {
  const img = event.target as HTMLImageElement
  img.src = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAwIiBoZWlnaHQ9IjIwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iMTAwJSIgaGVpZ2h0PSIxMDAlIiBmaWxsPSIjZGRkIi8+PHRleHQgeD0iNTAlIiB5PSI1MCUiIGZvbnQtZmFtaWx5PSJBcmlhbCIgZm9udC1zaXplPSIxNCIgZmlsbD0iIzk5OSIgdGV4dC1hbmNob3I9Im1pZGRsZSIgZHk9Ii4zZW0iPuWbvueJh+WKoOi9veWksei0pTwvdGV4dD48L3N2Zz4='
}

// 搜索轮椅
const searchWheelchairs = async () => {
  try {
    loading.value = true
    const response = await wheelchairApi.search({
      keyword: searchKeyword.value || undefined,
      sort_type: sortType.value || undefined,
      page: currentPage.value,
      limit: pageSize.value
    })
    
    if (response.code === 200 && response.data) {
      wheelchairs.value = response.data.list
      total.value = response.data.total
    } else {
      ElMessage.error(response.message || '获取轮椅列表失败')
    }
  } catch (error) {
    console.error('搜索轮椅失败:', error)
    ElMessage.error('搜索轮椅失败，请稍后重试')
  } finally {
    loading.value = false
  }
}

// 处理搜索
const handleSearch = () => {
  currentPage.value = 1
  searchWheelchairs()
}

// 处理页面大小变化
const handleSizeChange = (size: number) => {
  pageSize.value = size
  currentPage.value = 1
  searchWheelchairs()
}

// 处理页码变化
const handleCurrentChange = (page: number) => {
  currentPage.value = page
  searchWheelchairs()
}

// 查看详情
const viewDetail = (id: number) => {
  router.push(`/wheelchair/detail/${id}`)
}

// 组件挂载时获取数据
onMounted(() => {
  searchWheelchairs()
})
</script>

<style scoped>
.home-container {
  min-height: calc(100vh - 200px);
  background-color: #f5f7fa;
}

.content-wrapper {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.search-section {
  margin-bottom: 2rem;
}

.search-card {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.search-card :deep(.el-card__body) {
  padding: 2rem;
}

.search-header {
  text-align: center;
  margin-bottom: 2rem;
}

.search-header h2 {
  margin: 0 0 0.5rem 0;
  font-size: 2rem;
  font-weight: 600;
}

.search-header p {
  margin: 0;
  font-size: 1.1rem;
  opacity: 0.9;
}

.wheelchair-list {
  min-height: 400px;
}

.wheelchair-card {
  height: 100%;
  transition: transform 0.3s ease;
}

.wheelchair-card:hover {
  transform: translateY(-5px);
}

.wheelchair-image {
  height: 200px;
  overflow: hidden;
  border-radius: 8px;
  margin-bottom: 1rem;
}

.wheelchair-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.wheelchair-info {
  padding: 0.5rem 0;
}

.wheelchair-name {
  margin: 0 0 0.5rem 0;
  font-size: 1.2rem;
  font-weight: 600;
  color: #2c3e50;
}

.wheelchair-desc {
  margin: 0 0 0.5rem 0;
  color: #7f8c8d;
  font-size: 0.9rem;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.wheelchair-manufacturer {
  margin: 0 0 1rem 0;
  color: #95a5a6;
  font-size: 0.85rem;
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.wheelchair-details {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.price {
  display: flex;
  align-items: baseline;
  gap: 0.25rem;
}

.price-label {
  font-size: 0.9rem;
  color: #7f8c8d;
}

.price-value {
  font-size: 1.5rem;
  font-weight: 600;
  color: #e74c3c;
}

.price-unit {
  font-size: 0.8rem;
  color: #95a5a6;
}

.wheelchair-actions {
  margin-top: 1rem;
}

.pagination {
  display: flex;
  justify-content: center;
  margin-top: 2rem;
  padding: 2rem 0;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .content-wrapper {
    padding: 1rem;
  }
  
  .search-form .el-col {
    margin-bottom: 1rem;
  }
  
  .wheelchair-details {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }
}
</style>