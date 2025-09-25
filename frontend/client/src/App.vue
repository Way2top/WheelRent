<template>
  <div id="app">
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

const fontSizeStore = useFontSizeStore()

const fontSize = computed(() => fontSizeStore.size)

const setFontSize = (size: 'small' | 'default' | 'large') => {
  fontSizeStore.setSize(size)
}
</script>

<style scoped>
#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.app-header {
  background: linear-gradient(135deg, #409EFF 0%, #67C23A 100%);
  color: white;
  padding: 1rem 0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
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
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.app-main {
  flex: 1;
  background-color: #f5f7fa;
}

.app-footer {
  background-color: #2c3e50;
  color: white;
  text-align: center;
  padding: 2rem 0;
  margin-top: auto;
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
</style>