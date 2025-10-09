import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/user'

// 定义环境变量类型
interface ImportMetaEnv {
  readonly BASE_URL: string
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      redirect: '/home'
    },
    {
      path: '/home',
      name: 'Home',
      component: () => import('@/views/Home.vue')
    },
    {
      path: '/login',
      name: 'Login',
      component: () => import('@/views/Login.vue')
    },
    {
      path: '/wheelchair/detail/:id',
      name: 'WheelchairDetail',
      component: () => import('@/views/WheelchairDetail.vue')
    },
    {
      path: '/order/create',
      name: 'OrderCreate',
      component: () => import('@/views/OrderCreate.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/payment',
      name: 'Payment',
      component: () => import('@/views/Payment.vue'),
      meta: { requiresAuth: true }
    },
    { path: '/order/success', name: 'OrderSuccess', component: () => import('@/views/OrderSuccess.vue'), meta: { requiresAuth: true } },
    { path: '/test-order', name: 'TestOrder', component: () => import('@/views/TestOrder.vue') },
    { path: '/user-info', name: 'UserInfo', component: () => import('@/views/UserInfoManagement.vue'), meta: { requiresAuth: true } }
  ]
})

// 全局路由守卫
router.beforeEach(async (to, from, next) => {
  // 检查路由是否需要登录
  if (to.matched.some(record => record.meta.requiresAuth)) {
    const userStore = useUserStore()
    
    // 如果未登录，重定向到登录页
    if (!userStore.isLoggedIn) {
      next({
        path: '/login',
        query: { redirect: to.fullPath }
      })
      return
    }
    
    // 如果已登录但没有用户信息，尝试获取用户信息
    if (!userStore.user) {
      try {
        await userStore.getUserInfo()
      } catch (error) {
        console.error('获取用户信息失败:', error)
      }
    }
  }
  
  next()
})

export default router