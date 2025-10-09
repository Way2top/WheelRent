<template>
  <div id="app">
    <router-view />
  </div>
</template>

<script setup lang="ts">
// 管理端应用根组件
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
.font-size-small .card-header h2 { font-size: 1.3rem; }
.font-size-small .stat-card h3 { font-size: 1.1rem; }

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
.font-size-default .card-header h2 { font-size: 1.5rem; }
.font-size-default .stat-card h3 { font-size: 1.2rem; }

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
.font-size-large .card-header h2 { font-size: 1.7rem; }
.font-size-large .stat-card h3 { font-size: 1.3rem; }

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

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  background-color: #f9fafb;
  color: #1f2937;
}

#app {
  height: 100vh;
}

/* 页面容器 */
.page-container {
  padding: 1.5rem;
  background-color: #f9fafb;
  min-height: calc(100vh - 120px);
}

/* 卡片头部 */
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  padding: 0 0 1rem 0;
  border-bottom: 1px solid #e5e7eb;
}

.card-header h2 {
  margin: 0;
  color: #1f2937;
  font-size: 1.5rem;
  font-weight: 600;
}

/* 工具栏 */
.table-toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  padding: 1rem;
  background-color: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
}

/* 搜索表单 */
.search-form {
  display: flex;
  gap: 1rem;
  align-items: center;
  flex-wrap: wrap;
}

.search-form .el-form-item {
  margin-bottom: 0;
}

/* 分页容器 */
.pagination-container {
  display: flex;
  justify-content: center;
  margin-top: 2rem;
  padding: 1rem;
  background-color: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .page-container {
    padding: 1rem;
    margin-bottom: 1rem;
  }
  
  .table-toolbar {
    flex-direction: column;
    gap: 1rem;
  }
  
  .search-form {
    flex-wrap: wrap;
  }
}

/* Element Plus 样式覆盖 */
.el-button--primary {
  background-color: #059669;
  border-color: #059669;
}

.el-button--primary:hover {
  background-color: #047857;
  border-color: #047857;
}

.el-menu-item.is-active {
  background-color: #ecfdf5;
  color: #059669;
}

.el-menu-item:hover {
  background-color: #f0fdf4;
  color: #059669;
}

.el-card {
  border-radius: 12px;
  border: 1px solid #e5e7eb;
  box-shadow: none;
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

.font-size-large .table-toolbar {
  padding: 1.25rem;
}

.font-size-large .pagination-container {
  padding: 1.25rem;
}

/* Element Plus 样式覆盖 */
.el-button--primary {
  background-color: #059669;
  border-color: #059669;
}

.el-button--primary:hover {
  background-color: #047857;
  border-color: #047857;
}

.el-menu-item.is-active {
  background-color: #ecfdf5 !important;
  color: #059669 !important;
  border-right: 3px solid #059669;
}

.el-menu-item:hover {
  background-color: #f0fdf4 !important;
  color: #047857 !important;
}
</style>