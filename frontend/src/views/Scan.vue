<template>
  <el-card style="max-width:500px;margin:40px auto">
    <h3 style="text-align:center;margin-bottom:24px">扫码入库</h3>
    <el-input v-model="barcode" placeholder="扫描或输入条形码" size="large" autofocus clearable @keyup.enter="handleScan" />
    <el-button type="primary" size="large" style="width:100%;margin-top:16px" @click="handleScan" :loading="loading">确认入库</el-button>

    <el-alert v-if="result" :title="`${result.product} 入库成功，当前库存：${result.stock}`" type="success" style="margin-top:20px" show-icon />
  </el-card>
</template>

<script setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import api from '../api'

const barcode = ref('')
const loading = ref(false)
const result = ref(null)

async function handleScan() {
  if (!barcode.value.trim()) return
  loading.value = true
  result.value = null
  try {
    const res = await api.post('/inventory/scan/inbound/', { barcode: barcode.value.trim() })
    result.value = res
    barcode.value = ''
  } catch (e) {
    ElMessage.error(e.response?.data?.error || '扫码失败')
  } finally {
    loading.value = false
  }
}
</script>
