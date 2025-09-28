<template>
  <div style="padding: 20px;">
    <h1>测试订单API</h1>
    <button @click="testAPI" style="padding: 10px 20px; margin: 10px;">测试API调用</button>
    <div v-if="result" style="margin-top: 20px;">
      <h3>结果:</h3>
      <pre>{{ JSON.stringify(result, null, 2) }}</pre>
    </div>
    <div v-if="error" style="margin-top: 20px; color: red;">
      <h3>错误:</h3>
      <pre>{{ error }}</pre>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { orderApi } from '@/api/wheelchair'

const result = ref(null)
const error = ref('')

const testAPI = async () => {
  console.log('=== 开始测试API ===')
  result.value = null
  error.value = ''
  
  try {
    console.log('调用orderApi.getOrderDetail')
    const response = await orderApi.getOrderDetail('WR202509280846154457DB')
    console.log('API响应:', response)
    result.value = response
  } catch (err) {
    console.error('API调用失败:', err)
    error.value = err instanceof Error ? err.message : String(err)
  }
}
</script>