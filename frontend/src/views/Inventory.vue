<template>
  <div>
    <div style="display:flex;justify-content:space-between;margin-bottom:16px">
      <el-radio-group v-model="typeFilter" @change="fetchRecords">
        <el-radio-button value="">全部</el-radio-button>
        <el-radio-button value="in">入库</el-radio-button>
        <el-radio-button value="out">出库</el-radio-button>
      </el-radio-group>
      <el-button type="primary" @click="showForm = true">新建出入库</el-button>
    </div>

    <el-table :data="records" stripe v-loading="loading">
      <el-table-column prop="created_at" label="时间" width="160" />
      <el-table-column label="类型" width="80">
        <template #default="{row}">
          <el-tag :type="row.type === 'in' ? 'success' : 'warning'" size="small">{{ row.type === 'in' ? '入库' : '出库' }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="product_name" label="商品" />
      <el-table-column prop="quantity" label="数量" width="80" />
      <el-table-column prop="operator_name" label="操作人" width="100" />
      <el-table-column prop="remark" label="备注" />
    </el-table>

    <el-pagination style="margin-top:16px;justify-content:flex-end" :total="total" v-model:current-page="page" :page-size="10" layout="total, prev, pager, next" @current-change="fetchRecords" />

    <el-dialog v-model="showForm" title="新建出入库" width="450px">
      <el-form :model="form" label-width="80px">
        <el-form-item label="类型">
          <el-radio-group v-model="form.type">
            <el-radio value="in">入库</el-radio>
            <el-radio value="out">出库</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="商品ID"><el-input-number v-model="form.product" :min="1" /></el-form-item>
        <el-form-item label="数量"><el-input-number v-model="form.quantity" :min="1" /></el-form-item>
        <el-form-item label="单价"><el-input-number v-model="form.unit_price" :precision="2" :min="0" /></el-form-item>
        <el-form-item label="备注"><el-input v-model="form.remark" /></el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showForm = false">取消</el-button>
        <el-button type="primary" @click="submitRecord">提交</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import api from '../api'

const records = ref([])
const total = ref(0)
const page = ref(1)
const typeFilter = ref('')
const loading = ref(false)
const showForm = ref(false)
const form = reactive({ type: 'in', product: 1, quantity: 1, unit_price: 0, remark: '' })

async function fetchRecords() {
  loading.value = true
  const params = { page: page.value }
  if (typeFilter.value) params.type = typeFilter.value
  const res = await api.get('/inventory/records/', { params })
  records.value = res.results
  total.value = res.count
  loading.value = false
}

async function submitRecord() {
  await api.post('/inventory/records/', form)
  ElMessage.success('操作成功')
  showForm.value = false
  fetchRecords()
}

onMounted(fetchRecords)
</script>
