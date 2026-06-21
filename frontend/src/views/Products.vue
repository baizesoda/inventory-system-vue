<template>
  <div>
    <div style="display:flex;justify-content:space-between;margin-bottom:16px">
      <el-input v-model="search" placeholder="搜索商品名/SKU" style="width:300px" clearable @clear="fetchProducts" @keyup.enter="fetchProducts" />
      <el-button type="primary" @click="showForm = true">新增商品</el-button>
    </div>

    <el-table :data="products" stripe v-loading="loading">
      <el-table-column prop="sku" label="SKU" width="120" />
      <el-table-column prop="name" label="名称" />
      <el-table-column prop="category_name" label="分类" width="100" />
      <el-table-column prop="stock" label="库存" width="80" />
      <el-table-column prop="price" label="售价" width="80" />
      <el-table-column label="状态" width="100">
        <template #default="{row}">
          <el-tag :type="row.is_low_stock ? 'danger' : 'success'" size="small">
            {{ row.is_low_stock ? '库存不足' : '正常' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="120">
        <template #default="{row}">
          <el-button text size="small" @click="editProduct(row)">编辑</el-button>
          <el-button text size="small" type="danger" @click="deleteProduct(row.id)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-pagination style="margin-top:16px;justify-content:flex-end" :total="total" v-model:current-page="page" :page-size="10" layout="total, prev, pager, next" @current-change="fetchProducts" />

    <el-dialog v-model="showForm" :title="form.id ? '编辑商品' : '新增商品'" width="500px">
      <el-form :model="form" label-width="80px">
        <el-form-item label="SKU"><el-input v-model="form.sku" /></el-form-item>
        <el-form-item label="名称"><el-input v-model="form.name" /></el-form-item>
        <el-form-item label="条形码"><el-input v-model="form.barcode" /></el-form-item>
        <el-form-item label="规格"><el-input v-model="form.specification" /></el-form-item>
        <el-form-item label="售价"><el-input-number v-model="form.price" :precision="2" :min="0" /></el-form-item>
        <el-form-item label="成本"><el-input-number v-model="form.cost" :precision="2" :min="0" /></el-form-item>
        <el-form-item label="安全库存"><el-input-number v-model="form.safety_stock" :min="0" /></el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showForm = false">取消</el-button>
        <el-button type="primary" @click="saveProduct">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import api from '../api'

const products = ref([])
const total = ref(0)
const page = ref(1)
const search = ref('')
const loading = ref(false)
const showForm = ref(false)
const form = reactive({ id: null, sku: '', name: '', barcode: '', specification: '', price: 0, cost: 0, safety_stock: 10 })

async function fetchProducts() {
  loading.value = true
  const res = await api.get('/products/', { params: { page: page.value, search: search.value } })
  products.value = res.results
  total.value = res.count
  loading.value = false
}

function editProduct(row) {
  Object.assign(form, row)
  showForm.value = true
}

async function saveProduct() {
  if (form.id) {
    await api.put(`/products/${form.id}/`, form)
  } else {
    await api.post('/products/', form)
  }
  ElMessage.success('保存成功')
  showForm.value = false
  Object.assign(form, { id: null, sku: '', name: '', barcode: '', specification: '', price: 0, cost: 0, safety_stock: 10 })
  fetchProducts()
}

async function deleteProduct(id) {
  await ElMessageBox.confirm('确认删除?')
  await api.delete(`/products/${id}/`)
  ElMessage.success('已删除')
  fetchProducts()
}

onMounted(fetchProducts)
</script>
