<template>
  <div class="login-container">
    <div class="content-wrapper">
      <el-card class="login-card">
        <div class="login-header">
          <h2>{{ isRegister ? '用户注册' : '用户登录' }}</h2>
          <p>{{ isRegister ? '创建您的账户以开始租赁轮椅' : '登录您的账户以开始租赁轮椅' }}</p>
        </div>

        <el-form
          ref="formRef"
          :model="form"
          :rules="rules"
          label-position="top"
          @submit.prevent="handleSubmit"
        >
          <el-form-item label="用户名" prop="username">
            <el-input v-model="form.username" placeholder="请输入用户名" />
          </el-form-item>

          <el-form-item label="密码" prop="password">
            <el-input
              v-model="form.password"
              type="password"
              placeholder="请输入密码"
              show-password
            />
          </el-form-item>

          <template v-if="isRegister">
            <el-form-item label="手机号码" prop="phone">
              <el-input v-model="form.phone" placeholder="请输入手机号码" />
            </el-form-item>

            <el-form-item label="地址" prop="address">
              <el-input v-model="form.address" placeholder="请输入地址" />
            </el-form-item>
          </template>

          <div class="form-actions">
            <el-button
              type="primary"
              native-type="submit"
              :loading="loading"
              style="width: 100%"
            >
              {{ isRegister ? '注册' : '登录' }}
            </el-button>
          </div>

          <div class="form-footer">
            <span v-if="isRegister">
              已有账号？
              <el-button type="text" @click="isRegister = false">去登录</el-button>
            </span>
            <span v-else>
              没有账号？
              <el-button type="text" @click="isRegister = true">去注册</el-button>
            </span>
          </div>
        </el-form>
      </el-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()

// 表单引用
const formRef = ref()

// 是否为注册模式
const isRegister = ref(false)

// 加载状态
const loading = computed(() => userStore.loading)

// 表单数据
const form = reactive({
  username: '',
  password: '',
  phone: '',
  address: ''
})

// 表单验证规则
const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '用户名长度应为3-20个字符', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, max: 20, message: '密码长度应为6-20个字符', trigger: 'blur' }
  ],
  phone: [
    { pattern: /^1[3-9]\d{9}$/, message: '请输入有效的手机号码', trigger: 'blur' }
  ]
}

// 提交表单
const handleSubmit = async () => {
  if (!formRef.value) return
  
  try {
    await formRef.value.validate()
    
    let success = false
    
    if (isRegister.value) {
      // 注册
      success = await userStore.register({
        username: form.username,
        password: form.password,
        phone: form.phone || undefined,
        address: form.address || undefined
      })
      
      if (success) {
        ElMessage.success('注册成功')
      } else {
        ElMessage.error('注册失败，请稍后重试')
        return
      }
    } else {
      // 登录
      success = await userStore.login({
        username: form.username,
        password: form.password
      })
      
      if (success) {
        ElMessage.success('登录成功')
      } else {
        ElMessage.error('登录失败，用户名或密码错误')
        return
      }
    }
    
    // 登录或注册成功后，重定向到来源页面或首页
    const redirect = route.query.redirect as string
    router.replace(redirect || '/home')
    
  } catch (error) {
    console.error('表单验证失败:', error)
  }
}
</script>

<style scoped>
.login-container {
  min-height: calc(100vh - 200px);
  background-color: #f5f7fa;
  display: flex;
  align-items: center;
  justify-content: center;
}

.content-wrapper {
  width: 100%;
  max-width: 480px;
  margin: 2rem auto;
  padding: 0 1rem;
}

.login-card {
  border-radius: 12px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.05);
}

.login-card :deep(.el-card__body) {
  padding: 2rem;
}

.login-header {
  text-align: center;
  margin-bottom: 2rem;
}

.login-header h2 {
  margin: 0 0 0.5rem 0;
  font-size: 1.8rem;
  font-weight: 600;
  color: #2c3e50;
}

.login-header p {
  margin: 0;
  color: #7f8c8d;
  font-size: 1rem;
}

.form-actions {
  margin-top: 2rem;
}

.form-footer {
  margin-top: 1.5rem;
  text-align: center;
  color: #7f8c8d;
}
</style>