<template>
  <div id="app" :class="`font-size-${fontSize}`">
    <el-config-provider :size="fontSize">
      <div class="app-header">
        <div class="header-content">
          <div class="logo">
            <h1>在线轮椅租赁系统</h1>
          </div>
          <div class="header-actions">
            <el-button-group>
              <el-button 
                :type="fontSize === 'default' ? 'primary' : ''"
                @click="setFontSize('default')"
              >
                标准字体
              </el-button>
              <el-button 
                :type="fontSize === 'large' ? 'primary' : ''"
                @click="setFontSize('large')"
              >
                大字体
              </el-button>
              <el-button 
                :type="fontSize === 'small' ? 'primary' : ''"
                @click="setFontSize('small')"
              >
                小字体
              </el-button>
            </el-button-group>
          </div>
        </div>
      </div>
      
      <!-- 导航栏 -->
      <NavBar />
      
      <div class="app-main">
        <router-view />
      </div>
      
      <div class="app-footer">
        <p>&copy; 2025 在线轮椅租赁系统. 专为失能老人提供便捷的轮椅租赁服务.</p>
      </div>
    </el-config-provider>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useFontSizeStore } from '@/stores/fontSize'
import NavBar from '@/components/NavBar.vue'

const fontSizeStore = useFontSizeStore()

const fontSize = computed(() => fontSizeStore.size)

const setFontSize = (size: 'small' | 'default' | 'large') => {
  fontSizeStore.setSize(size)
}
</script>

<style>
/* 全局字体大小样式 */
.font-size-small {
  font-size: 14px;
}

.font-size-small h1 { font-size: 1.8rem; }
.font-size-small h2 { font-size: 1.5rem; }
.font-size-small h3 { font-size: 1.3rem; }
.font-size-small .el-button { font-size: 14px; }
.font-size-small .el-input__inner { font-size: 14px; }
.font-size-small .el-form-item__label { font-size: 14px; }
.font-size-small .el-card__header { font-size: 1.1rem; }
.font-size-small .wheelchair-name { font-size: 1.1rem; }
.font-size-small .price-value { font-size: 1.3rem; }
.font-size-small .search-header h2 { font-size: 1.8rem; }

.font-size-default {
  font-size: 16px;
}

.font-size-default h1 { font-size: 2rem; }
.font-size-default h2 { font-size: 1.8rem; }
.font-size-default h3 { font-size: 1.5rem; }
.font-size-default .el-button { font-size: 16px; }
.font-size-default .el-input__inner { font-size: 16px; }
.font-size-default .el-form-item__label { font-size: 16px; }
.font-size-default .el-card__header { font-size: 1.2rem; }
.font-size-default .wheelchair-name { font-size: 1.2rem; }
.font-size-default .price-value { font-size: 1.5rem; }
.font-size-default .search-header h2 { font-size: 2rem; }

.font-size-large {
  font-size: 18px;
}

.font-size-large h1 { font-size: 2.2rem; }
.font-size-large h2 { font-size: 2rem; }
.font-size-large h3 { font-size: 1.8rem; }
.font-size-large .el-button { font-size: 18px; }
.font-size-large .el-input__inner { font-size: 18px; }
.font-size-large .el-form-item__label { font-size: 18px; }
.font-size-large .el-card__header { font-size: 1.3rem; }
.font-size-large .wheelchair-name { font-size: 1.3rem; }
.font-size-large .price-value { font-size: 1.8rem; }
.font-size-large .search-header h2 { font-size: 2.2rem; }

.font-size-large .header-content {
  padding: 0 1.5rem;
}

.font-size-large .font-controls button {
  padding: 0.75rem 1.25rem;
  font-size: 18px;
}

.font-size-large .el-form-item__label {
  line-height: 1.8;
}

.font-size-large .el-input__inner {
  padding: 12px 16px;
}

.font-size-large .el-button--large {
  padding: 16px 24px;
  min-height: 50px;
}

.app-header {
  background: #ffffff;
  color: #059669;
  padding: 1rem 0;
  border-bottom: 1px solid #e5e7eb;
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo h1 {
  margin: 0;
  font-size: 1.8rem;
  font-weight: 600;
  color: #059669;
  letter-spacing: -0.5px;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.app-main {
  flex: 1;
  background-color: #f9fafb;
}

.app-footer {
  background-color: #ffffff;
  color: #6b7280;
  text-align: center;
  padding: 2rem 0;
  margin-top: auto;
  border-top: 1px solid #e5e7eb;
}

.app-footer p {
  margin: 0;
  font-size: 0.9rem;
}

/* 大字模式样式 */
:deep(.el-config-provider[data-size="large"]) {
  --el-font-size-base: 18px;
  --el-font-size-small: 16px;
  --el-font-size-large: 20px;
  --el-component-size: 48px;
}

:deep(.el-config-provider[data-size="small"]) {
  --el-font-size-base: 12px;
  --el-font-size-small: 10px;
  --el-font-size-large: 14px;
  --el-component-size: 28px;
}

/* Element Plus 样式优化 */
:deep(.el-button--primary) {
  background-color: #059669;
  border-color: #059669;
}

:deep(.el-button--primary:hover) {
  background-color: #047857;
  border-color: #047857;
}

:deep(.el-card) {
  border-radius: 12px;
  border: 1px solid #e5e7eb;
}

/* 大字模式下的表格和表单优化 */
.font-size-large .el-table {
  font-size: 18px;
}

.font-size-large .el-table th {
  padding: 16px 12px;
}

.font-size-large .el-table td {
  padding: 14px 12px;
}

.font-size-large .el-pagination {
  font-size: 18px;
}

.font-size-large .el-pagination button {
  min-width: 40px;
  min-height: 40px;
}

.font-size-large .el-dialog__header {
  font-size: 1.3rem;
  padding: 20px 24px;
}

.font-size-large .el-dialog__body {
  font-size: 18px;
  padding: 24px;
}

.font-size-large .el-dialog__footer {
  padding: 16px 24px;
}
</style>