import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      redirect: '/login'
    },
    {
      path: '/login',
      name: 'Login',
      component: () => import('@/views/Login.vue'),
      meta: {
        title: '管理员登录',
        requiresAuth: false
      }
    },
    {
      path: '/dashboard',
      name: 'Dashboard',
      component: () => import('@/views/Layout.vue'),
      meta: {
        title: '管理后台',
        requiresAuth: true
      },
      children: [
        {
          path: '',
          name: 'DashboardHome',
          component: () => import('@/views/Dashboard.vue'),
          meta: {
            title: '数据概览',
            requiresAuth: true
          }
        },
        {
          path: 'wheelchairs',
          name: 'WheelchairManagement',
          component: () => import('@/views/WheelchairManagement.vue'),
          meta: {
            title: '轮椅管理',
            requiresAuth: true
          }
        },
        {
          path: 'orders',
          name: 'OrderManagement',
          component: () => import('@/views/OrderManagement.vue'),
          meta: {
            title: '订单管理',
            requiresAuth: true
          }
        },
        {
          path: 'users',
          name: 'UserManagement',
          component: () => import('@/views/UserManagement.vue'),
          meta: {
            title: '用户管理',
            requiresAuth: true
          }
        },
        {
          path: 'settings',
          name: 'SystemSettings',
          component: () => import('@/views/SystemSettings.vue'),
          meta: {
            title: '系统设置',
            requiresAuth: true
          }
        }
      ]
    }
  ]
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  
  // 设置页面标题
  if (to.meta.title) {
    document.title = `${to.meta.title} - 在线轮椅租赁系统管理后台`
  }
  
  // 检查是否需要登录
  if (to.meta.requiresAuth) {
    if (authStore.isLoggedIn) {
      next()
    } else {
      next('/login')
    }
  } else {
    // 如果已登录且访问登录页，重定向到仪表板
    if (to.path === '/login' && authStore.isLoggedIn) {
      next('/dashboard')
    } else {
      next()
    }
  }
})

export default router