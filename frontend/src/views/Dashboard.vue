<template>
  <div>
    <el-row :gutter="20" style="margin-bottom:20px">
      <el-col :span="6">
        <el-card shadow="hover"><el-statistic title="商品总数" :value="data.total_products" /></el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover"><el-statistic title="库存总值 (元)" :value="data.total_value" :precision="2" /></el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover"><el-statistic title="今日入库" :value="data.today_in" /></el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover"><el-statistic title="今日出库" :value="data.today_out" /></el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20">
      <el-col :span="12">
        <el-card header="低库存预警">
          <el-table :data="data.low_stock" size="small" stripe>
            <el-table-column prop="name" label="商品" />
            <el-table-column prop="stock" label="当前" width="80" />
            <el-table-column prop="safety_stock" label="安全值" width="80" />
          </el-table>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card header="分类统计">
          <el-table :data="data.categories" size="small" stripe>
            <el-table-column prop="name" label="分类" />
            <el-table-column prop="product_count" label="商品数" width="80" />
            <el-table-column prop="total_stock" label="总库存" width="80" />
          </el-table>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { reactive, onMounted } from 'vue'
import api from '../api'

const data = reactive({
  total_products: 0, total_value: 0, today_in: 0, today_out: 0,
  low_stock: [], categories: [],
})

onMounted(async () => {
  const res = await api.get('/dashboard/overview/')
  Object.assign(data, res)
})
</script>
