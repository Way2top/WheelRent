import { createRouter, createWebHistory } from 'vue-router'
import Home from '@/views/Home.vue'

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
      component: Home
    },
    {
      path: '/wheelchair/detail/:id',
      name: 'WheelchairDetail',
      component: () => import('@/views/WheelchairDetail.vue')
    },
    {
      path: '/order/create',
      name: 'OrderCreate',
      component: () => import('@/views/OrderCreate.vue')
    },
    {
      path: '/payment',
      name: 'Payment',
      component: () => import('@/views/Payment.vue')
    },
    {
      path: '/order/success',
      name: 'OrderSuccess',
      component: () => import('@/views/OrderSuccess.vue')
    },
    {
      path: '/test-order',
      name: 'TestOrder',
      component: () => import('@/views/TestOrder.vue')
    }
  ]
})

export default router