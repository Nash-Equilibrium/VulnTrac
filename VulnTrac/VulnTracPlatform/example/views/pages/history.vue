<template>
  <el-card class="history-card">
    <template #header>
      <div class="card-header">
        <el-text tag="b" size="large" type="primary">检测记录</el-text>
        <el-text size="small">提示: 个人检测报告系统为您保留14天!（不含检测完成当天），请您及时下载保存!</el-text>
      </div>
    </template>

    <div class="filter-bar">
      <el-date-picker v-model="dateRange" type="daterange" range-separator="至" start-placeholder="开始时间" end-placeholder="结束时间" />
      <el-select v-model="status" placeholder="状态" class="status-select">
        <el-option label="全部" value="all"></el-option>
        <el-option label="已完成" value="completed"></el-option>
        <el-option label="已取消" value="canceled"></el-option>
        <el-option label="待支付" value="pending"></el-option>
      </el-select>
      <el-select v-model="sortOrder" placeholder="排序方式" class="sort-select">
        <el-option label="上传时间" value="uploadTime"></el-option>
        <el-option label="项目名" value="projectName"></el-option>
        <el-option label="状态" value="status"></el-option>
      </el-select>
      <el-input v-model="search" placeholder="项目名/用户名搜索" class="search-input" />
      <el-button @click="filterRecords" type="primary">确定</el-button>
      <el-button @click="resetFilters">重置</el-button>
    </div>

    <div v-for="record in paginatedRecords" :key="record.id" class="record-card">
      <el-card shadow="always" class="record-el-card">
        <div class="record-header">
          <div class="record-info">
            <el-link :underline="false">{{ record.projectName || '无项目名' }}</el-link>
            <el-tag type="success">{{ record.statusText }}</el-tag>
          </div>
          <div class="record-stats">
            <el-tag type="info">{{ record.username || '匿名用户' }}</el-tag>
            <el-tag type="info">{{ new Date(record.detectionDate).toLocaleDateString() }}</el-tag>
            <el-tag type="danger">高危缺陷数量: {{ record.highRiskDefects }}</el-tag>
            <el-tag type="warning">中危缺陷数量: {{ record.mediumRiskDefects }}</el-tag>
            <el-tag type="info">低危缺陷数量: {{ record.lowRiskDefects }}</el-tag>
          </div>
        </div>
        <div class="record-body">
          <div class="record-actions">
            <el-button type="text" @click="viewReport(record.pdfUrl)">查看报告</el-button>
            <el-button type="text" @click="confirmDeleteRecord(record.id)" icon="el-icon-delete">删除</el-button>
          </div>
        </div>
      </el-card>
    </div>

    <div class="demo-pagination-block">
      <el-pagination v-model:current-page="currentPage" v-model:page-size="pageSize" :page-sizes="[5, 10, 15, 20]" :background="true" layout="total, sizes, prev, pager, next, jumper" :total="totalRecords" @size-change="handleSizeChange" @current-change="handleCurrentChange" />
    </div>
  </el-card>
</template>

<script lang="ts" setup>
import { ref, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'

const dateRange = ref([])
const status = ref('all')
const search = ref('')
const sortOrder = ref('uploadTime')  // 默认按上传时间排序
const currentPage = ref(1)
const pageSize = ref(5)  // 设置每页显示5个记录

// 伪造的数据
const records = ref([
  {
    id: 1,
    projectName: '项目A',
    username: '用户1',
    detectionDate: '2023-06-01T10:00:00Z',
    highRiskDefects: 5,
    mediumRiskDefects: 10,
    lowRiskDefects: 15,
    pdfUrl: 'https://example.com/report1.pdf',
    status: 'completed',
    uploadTime: '2023-06-01T10:00:00Z'
  },
  {
    id: 2,
    projectName: '项目B',
    username: '用户2',
    detectionDate: '2023-06-02T11:00:00Z',
    highRiskDefects: 3,
    mediumRiskDefects: 7,
    lowRiskDefects: 8,
    pdfUrl: 'https://example.com/report2.pdf',
    status: 'canceled',
    uploadTime: '2023-06-02T11:00:00Z'
  },
  {
    id: 3,
    projectName: '项目C',
    username: '用户3',
    detectionDate: '2023-06-03T12:00:00Z',
    highRiskDefects: 6,
    mediumRiskDefects: 9,
    lowRiskDefects: 12,
    pdfUrl: 'https://example.com/report3.pdf',
    status: 'pending',
    uploadTime: '2023-06-03T12:00:00Z'
  }
])

// 按选择的排序方式排序记录
const sortedRecords = computed(() => {
  let sorted = [...records.value]
  if (sortOrder.value === 'uploadTime') {
    sorted.sort((a, b) => new Date(b.uploadTime).getTime() - new Date(a.uploadTime).getTime())
  } else if (sortOrder.value === 'projectName') {
    sorted.sort((a, b) => a.projectName.localeCompare(b.projectName))
  } else if (sortOrder.value === 'status') {
    sorted.sort((a, b) => a.status.localeCompare(b.status))
  }
  return sorted
})

const filteredRecords = computed(() => {
  let result = sortedRecords.value

  if (dateRange.value.length === 2) {
    const [start, end] = dateRange.value
    result = result.filter(record => new Date(record.uploadTime) >= new Date(start) && new Date(record.uploadTime) <= new Date(end))
  }

  if (status.value !== 'all') {
    result = result.filter(record => record.status === status.value)
  }

  if (search.value) {
    result = result.filter(record => record.projectName.includes(search.value) || record.username.includes(search.value))
  }

  return result
})

// 分页记录
const paginatedRecords = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value
  const end = start + pageSize.value
  return filteredRecords.value.slice(start, end)
})

const totalRecords = computed(() => filteredRecords.value.length)

const filterRecords = () => {
  currentPage.value = 1
}

const resetFilters = () => {
  dateRange.value = []
  status.value = 'all'
  search.value = ''
  currentPage.value = 1
}

const handlePageChange = (page: number) => {
  currentPage.value = page
}

const handleSizeChange = (size: number) => {
  pageSize.value = size
}

const viewReport = (pdfUrl: string) => {
  if (pdfUrl) {
    window.open(pdfUrl, '_blank')
  } else {
    ElMessage.warning('该报告没有有效的PDF链接')
  }
}

const confirmDeleteRecord = (id: number) => {
  ElMessageBox.confirm('此操作将永久删除该记录, 是否继续?', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning',
  })
    .then(() => {
      deleteRecord(id)
      ElMessage.success('记录已删除')
    })
    .catch(() => {
      ElMessage.info('已取消删除')
    })
}

const deleteRecord = (id: number) => {
  records.value = records.value.filter(record => record.id !== id)
}

const payForReport = (id: number) => {
  ElMessage.info(`付费获取报告 ID: ${id}`)
}
</script>

<style scoped>
.history-container {
  padding: 20px;
  background-color: #f0f2f5;
}

.history-card {
  padding: 20px;
  border-radius: 8px;
}

.card-header {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 20px;
}

.filter-bar {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 20px;
}

.status-select,
.sort-select {
  width: 180px;
}

.search-input {
  width: 300px;
}

.record-card {
  margin-bottom: 20px;
}

.record-el-card {
  background-color: #fff;
  border: 1px solid #ebeef5;
  border-radius: 8px;
}

.record-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px;
  background-color: #fafafa;
  border-bottom: 1px solid #ebeef5;
}

.record-info {
  display: flex;
  flex-direction: column;
}

.record-stats {
  display: flex;
  gap: 10px;
}

.record-body {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px;
}

.record-actions {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.demo-pagination-block {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 20px;
}
</style>
