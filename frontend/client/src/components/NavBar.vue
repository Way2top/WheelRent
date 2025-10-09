<template>
  <div class="navbar">
    <div class="navbar-content">
      <div class="navbar-left">
        <router-link to="/home" class="nav-link">首页</router-link>
      </div>
      <div class="navbar-right">
        <template v-if="userStore.isLoggedIn">
          <el-dropdown>
            <span class="user-dropdown-link">
              {{ userStore.user?.username || '用户' }}
              <el-icon class="el-icon--right"><arrow-down /></el-icon>
            </span>
            <template #dropdown>
              <el-dropdown-menu>
              <el-dropdown-item @click="toUserInfo">信息管理</el-dropdown-item>
              <el-dropdown-item @click="logout">退出登录</el-dropdown-item>
            </el-dropdown-menu>
            </template>
          </el-dropdown>
        </template>
        <template v-else>
          <router-link to="/login" class="nav-link">登录/注册</router-link>
        </template>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ArrowDown } from '@element-plus/icons-vue'
import { useUserStore } from '@/stores/user'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'

const userStore = useUserStore()
const router = useRouter()

const logout = async () => {
  userStore.logout()
  ElMessage.success('已退出登录')
  router.push('/home')
}

const toUserInfo = () => {
  router.push('/user-info')
}
</script>

<style scoped>
.navbar {
  background-color: #ffffff;
  border-bottom: 1px solid #e5e7eb;
  padding: 0.75rem 0;
}

.navbar-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.navbar-left, .navbar-right {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.nav-link {
  color: #374151;
  text-decoration: none;
  font-weight: 500;
  padding: 0.5rem 0;
  transition: color 0.2s ease;
}

.nav-link:hover {
  color: #059669;
}

.user-dropdown-link {
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #374151;
  font-weight: 500;
  transition: color 0.2s ease;
}

.user-dropdown-link:hover {
  color: #059669;
}
</style>