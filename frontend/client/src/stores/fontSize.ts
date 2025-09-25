import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useFontSizeStore = defineStore('fontSize', () => {
  const size = ref<'small' | 'default' | 'large'>('default')

  const setSize = (newSize: 'small' | 'default' | 'large') => {
    size.value = newSize
    // 保存到本地存储
    localStorage.setItem('fontSize', newSize)
  }

  const initSize = () => {
    const savedSize = localStorage.getItem('fontSize') as 'small' | 'default' | 'large'
    if (savedSize && ['small', 'default', 'large'].includes(savedSize)) {
      size.value = savedSize
    }
  }

  // 初始化时从本地存储读取
  initSize()

  return {
    size,
    setSize,
    initSize
  }
})