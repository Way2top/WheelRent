<template>
  <div class="login-container">
    <div class="login-wrapper">
      <div class="login-card">
        <!-- 头部标题 -->
        <div class="login-header">
          <div class="logo">
            <el-icon size="48" color="#409EFF">
              <Management />
            </el-icon>
          </div>
          <h1 class="title">在线轮椅租赁系统</h1>
          <p class="subtitle">管理后台</p>
        </div>
        
        <!-- 登录表单 -->
        <el-form
          ref="loginFormRef"
          :model="loginForm"
          :rules="loginRules"
          class="login-form"
          size="large"
          @keyup.enter="handleLogin"
        >
          <el-form-item prop="username">
            <el-input
              v-model="loginForm.username"
              placeholder="请输入用户名"
              prefix-icon="User"
              clearable
            />
          </el-form-item>
          
          <el-form-item prop="password">
            <el-input
              v-model="loginForm.password"
              type="password"
              placeholder="请输入密码"
              prefix-icon="Lock"
              show-password
              clearable
            />
          </el-form-item>
          
          <el-form-item>
            <el-checkbox v-model="rememberMe">
              记住我
            </el-checkbox>
          </el-form-item>
          
          <el-form-item>
            <el-button
              type="primary"
              class="login-button"
              :loading="loading"
              @click="handleLogin"
            >
              {{ loading ? '登录中...' : '登录' }}
            </el-button>
          </el-form-item>
        </el-form>
        
        <!-- 底部信息 -->
        <div class="login-footer">
          <p class="demo-info">
            <el-icon><InfoFilled /></el-icon>
            演示账号：admin / 123456
          </p>
          <p class="copyright">
            © 2024 在线轮椅租赁系统. All rights reserved.
          </p>
        </div>
      </div>
    </div>
    
    <!-- 背景装饰 -->
    <div class="background-decoration">
      <div class="decoration-circle circle-1"></div>
      <div class="decoration-circle circle-2"></div>
      <div class="decoration-circle circle-3"></div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, type FormInstance, type FormRules } from 'element-plus'
import { Management, InfoFilled } from '@element-plus/icons-vue'
import { useAuthStore } from '@/stores/auth'
import { authApi } from '@/api'
import type { LoginRequest } from '@/types/api'

const router = useRouter()
const authStore = useAuthStore()

// 响应式数据
const loginFormRef = ref<FormInstance>()
const loading = ref(false)
const rememberMe = ref(false)

// 登录表单数据
const loginForm = reactive<LoginRequest>({
  username: '',
  password: ''
})

// 表单验证规则
const loginRules: FormRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '用户名长度在 3 到 20 个字符', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, max: 20, message: '密码长度在 6 到 20 个字符', trigger: 'blur' }
  ]
}

// 处理登录
const handleLogin = async () => {
  if (!loginFormRef.value) return
  
  try {
    const valid = await loginFormRef.value.validate()
    if (!valid) return
    
    loading.value = true
    
    const response = await authApi.login(loginForm)
    
    if (response.code === 200 && response.data) {
      const { token, user } = response.data
      
      // 保存登录状态
      authStore.login(token, user)
      
      // 记住我功能
      if (rememberMe.value) {
        localStorage.setItem('remember_username', loginForm.username)
      } else {
        localStorage.removeItem('remember_username')
      }
      
      ElMessage.success('登录成功')
      
      // 跳转到仪表板
      router.push('/dashboard')
    } else {
      ElMessage.error(response.message || '登录失败')
    }
  } catch (error: any) {
    console.error('登录失败:', error)
    ElMessage.error(error.response?.data?.message || '登录失败，请稍后重试')
  } finally {
    loading.value = false
  }
}

// 初始化
onMounted(() => {
  // 如果已登录，直接跳转到仪表板
  if (authStore.isLoggedIn) {
    router.push('/dashboard')
    return
  }
  
  // 恢复记住的用户名
  const rememberedUsername = localStorage.getItem('remember_username')
  if (rememberedUsername) {
    loginForm.username = rememberedUsername
    rememberMe.value = true
  }
  
  // 演示数据预填充
  if (!loginForm.username) {
    loginForm.username = 'admin'
    loginForm.password = '123456'
  }
})
</script>

<style scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  position: relative;
  overflow: hidden;
}

.login-wrapper {
  position: relative;
  z-index: 10;
}

.login-card {
  width: 400px;
  padding: 40px;
  background: rgba(255, 255, 255, 0.95);
  border-radius: 16px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.login-header {
  text-align: center;
  margin-bottom: 40px;
}

.logo {
  margin-bottom: 16px;
}

.title {
  font-size: 28px;
  font-weight: 600;
  color: #2c3e50;
  margin: 0 0 8px 0;
}

.subtitle {
  font-size: 16px;
  color: #7f8c8d;
  margin: 0;
}

.login-form {
  margin-bottom: 30px;
}

.login-form .el-form-item {
  margin-bottom: 24px;
}

.login-button {
  width: 100%;
  height: 48px;
  font-size: 16px;
  font-weight: 500;
  border-radius: 8px;
}

.login-footer {
  text-align: center;
}

.demo-info {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  margin: 0 0 16px 0;
  padding: 12px;
  background-color: #e1f3ff;
  border: 1px solid #b3d8ff;
  border-radius: 8px;
  color: #409eff;
  font-size: 14px;
}

.copyright {
  font-size: 12px;
  color: #95a5a6;
  margin: 0;
}

.background-decoration {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
}

.decoration-circle {
  position: absolute;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.1);
  animation: float 6s ease-in-out infinite;
}

.circle-1 {
  width: 200px;
  height: 200px;
  top: 10%;
  left: 10%;
  animation-delay: 0s;
}

.circle-2 {
  width: 150px;
  height: 150px;
  top: 60%;
  right: 10%;
  animation-delay: 2s;
}

.circle-3 {
  width: 100px;
  height: 100px;
  bottom: 20%;
  left: 20%;
  animation-delay: 4s;
}

@keyframes float {
  0%, 100% {
    transform: translateY(0px) rotate(0deg);
  }
  50% {
    transform: translateY(-20px) rotate(180deg);
  }
}

/* 响应式设计 */
@media (max-width: 480px) {
  .login-card {
    width: 90%;
    padding: 30px 20px;
    margin: 20px;
  }
  
  .title {
    font-size: 24px;
  }
  
  .subtitle {
    font-size: 14px;
  }
}

/* 深色模式适配 */
@media (prefers-color-scheme: dark) {
  .login-card {
    background: rgba(30, 30, 30, 0.95);
    border: 1px solid rgba(255, 255, 255, 0.1);
  }
  
  .title {
    color: #ecf0f1;
  }
  
  .subtitle {
    color: #bdc3c7;
  }
  
  .copyright {
    color: #7f8c8d;
  }
}
</style>