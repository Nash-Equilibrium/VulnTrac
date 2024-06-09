<template>
  <div class="repo-total">
    <el-card class="box-card">
      <template #header>
        <div class="flex justify-between">
          <h2 class="header">仓库监测数据</h2>
          <p class="info">提示：您可以在此查看相应数据。</p>
        </div>
      </template>
      <div class="repo-show">
        <div v-for="item in items" :key="item.id" class="repo-data">
          <div class="card">
            <h3 class="card__title" style="margin-top: -8px;">{{ item.title }}</h3>
            <p class="card__content" style="margin-top: -12px">{{ item.description }}</p>
            <tiny-statistic :value="item.value"
              :value-style="[{ 'color': '#3ac295', 'text-align': 'end', 'width': '50%' }]">
              <template #suffix><span style="font-size: 20px"> {{ item.unit }} </span></template>
            </tiny-statistic>
            <div class="card__date"></div>
            <div class="card__arrow"></div>
          </div>
        </div>
      </div>
      <div class="repo-graph">
        <el-card class="map">
          <template #header>
            <div class="header">近14天检测项目数量</div>
          </template>
          <div>
            <tiny-chart-line :options="lineOptions"></tiny-chart-line>
          </div>
        </el-card>
        <el-card class="map">
          <template #header>
            <div class="header">近14天检测项目情况</div>
          </template>
          <div>
            <tiny-chart-pie :color-mode="pieColor" :options="pieOptions"></tiny-chart-pie>
          </div>
        </el-card>
      </div>
    </el-card>
  </div>
  <div class="repo-management">
    <el-card class="box-card">
      <template #header>
        <h2 class="header">仓库管理</h2>
        <p class="info">提示：您可以在此管理您的仓库信息，并执行相关操作。</p>
      </template>
      <el-row :gutter="24" class="filter-row">
        <el-col :span="8">
          <el-date-picker v-model="dateRange" type="daterange" range-separator="至" start-placeholder="开始时间"
            end-placeholder="结束时间" style="width: 100%;" />
        </el-col>
        <el-col :span="4">
          <el-select v-model="filterType" placeholder="仓库类型" style="width: 100%;">
            <el-option label="全部" value=""></el-option>
            <el-option label="GitHub" value="github"></el-option>
            <el-option label="GitLab" value="gitlab"></el-option>
            <el-option label="Gitee" value="gitee"></el-option>
          </el-select>
        </el-col>
        <el-col :span="6">
          <el-input v-model="searchQuery" placeholder="搜索仓库名称或描述" style="width: 100%;" />
        </el-col>
        <el-col :span="2">
          <el-button type="primary" @click="searchRepos" style="width: 100%;">搜索</el-button>
        </el-col>
        <el-col :span="2">
          <el-button @click="resetFilters" style="width: 100%;">重置</el-button>
        </el-col>
        <el-col :span="2" class="align-right">
          <el-button type="primary" @click="openAddEditRepo(null)" icon="el-icon-plus"
            style="width: 100%;">添加仓库</el-button>
        </el-col>
      </el-row>

      <el-table :data="filteredRepos" stripe style="width: 100%; margin-top: 20px;">
        <el-table-column prop="name" label="名称" width="180"></el-table-column>
        <el-table-column prop="description" label="描述"></el-table-column>
        <el-table-column prop="created_at" label="创建时间" width="180"></el-table-column>
        <el-table-column fixed="right" label="操作" width="230">
          <template #default="scope">
            <el-button @click="openAddEditRepo(scope.row)" size="small">编辑</el-button>
            <el-button @click="confirmDeleteRepo(scope.row.id)" type="danger" size="small">删除</el-button>
            <el-button @click="openRepoDetail(scope.row)" type="info" size="small">详情</el-button>
          </template>
        </el-table-column>
      </el-table>

      <el-pagination background layout="total, sizes, prev, pager, next, jumper" :total="reposTotal"
        :page-sizes="[5, 10, 20, 50]" v-model:page-size="pageSize" v-model:current-page="currentPage"
        style="margin-top: 20px;" />
    </el-card>

    <!-- 添加/编辑仓库对话框 -->
    <el-dialog v-model="showAddEditRepo" title="添加/编辑仓库" width="500" :before-close="handleClose">
      <el-form :model="form" :rules="rules" ref="formRef" label-width="80px">
        <el-form-item label="名称" prop="name">
          <el-input v-model="form.name"></el-input>
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input v-model="form.description"></el-input>
        </el-form-item>
        <el-form-item label="URL" prop="url">
          <el-input v-model="form.url"></el-input>
        </el-form-item>
        <el-form-item label="类型" prop="type">
          <el-select v-model="form.type">
            <el-option label="GitHub" value="github"></el-option>
            <el-option label="GitLab" value="gitlab"></el-option>
            <el-option label="Gitee" value="gitee"></el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="closeAddEditRepo">取消</el-button>
          <el-button type="primary" @click="saveRepo">保存</el-button>
        </div>
      </template>
    </el-dialog>

    <!-- 仓库详情对话框 -->
    <el-dialog v-model="showRepoDetail" title="仓库详情" width="500" :before-close="handleClose">
      <div>
        <p><strong>名称:</strong> {{ selectedRepo?.name }}</p>
        <p><strong>描述:</strong> {{ selectedRepo?.description }}</p>
        <p><strong>URL:</strong> <a :href="selectedRepo?.url" target="_blank">{{ selectedRepo?.url }}</a></p>
        <p><strong>类型:</strong> {{ selectedRepo?.type }}</p>
        <p><strong>状态:</strong> {{ selectedRepo?.status }}</p>
        <p><strong>创建时间:</strong> {{ selectedRepo?.created_at }}</p>
      </div>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="closeRepoDetail">关闭</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import { useStore } from 'vuex';
import { ElMessageBox, ElMessage } from 'element-plus';

interface Repo {
  id?: number;
  name: string;
  description: string;
  url: string;
  type: string;
  status?: string;
  created_at?: string;
}

// 展示
const items = ref([
  { id: 1, description: 'VulnTrac监测的仓库总数', title: '监测中仓库', value: 7, unit: '个' },
  { id: 2, description: 'VulnTrac已经执行的监测次数', title: '监测总次数', value: 41, unit: '次' },
  { id: 3, description: 'VulnTrac发现的缺陷数', title: '发现缺陷数', value: 17, unit: '个' },
]);

const store = useStore();
const searchQuery = ref('');
const filterType = ref('');
const dateRange = ref<[Date, Date] | null>(null);
const showAddEditRepo = ref(false);
const showRepoDetail = ref(false);
const selectedRepo = ref<Repo | null>(null);
const pageSize = ref(5);
const currentPage = ref(1);
const formRef = ref<any>(null); // Ensure ref is declared here
const form = ref<Repo>({ name: '', description: '', url: '', type: '' });

const rules = {
  name: [{ required: true, message: '请输入名称', trigger: 'blur' }],
  description: [{ required: true, message: '请输入描述', trigger: 'blur' }],
  url: [{ required: true, message: '请输入URL', trigger: 'blur' }],
  type: [{ required: true, message: '请选择类型', trigger: 'change' }],
};

const repos = computed(() => store.state.repos || [
  { id: 1, name: 'Repo1', description: '这是第一个仓库', url: 'https://github.com/repo1', type: 'github', status: 'active', created_at: '2023-01-01' },
  { id: 2, name: 'Repo2', description: '这是第二个仓库', url: 'https://gitlab.com/repo2', type: 'gitlab', status: 'active', created_at: '2023-02-01' },
  { id: 3, name: 'Repo3', description: '这是第三个仓库', url: 'https://gitee.com/repo3', type: 'gitee', status: 'inactive', created_at: '2023-03-01' },
  { id: 4, name: 'FakeRepo', description: '这是一个伪造的仓库', url: 'https://example.com/fakerepo', type: 'github', status: 'active', created_at: '2023-04-01' },
  { id: 5, name: 'TestRepo', description: '这是一个测试仓库', url: 'https://example.com/testrepo', type: 'gitlab', status: 'active', created_at: '2023-05-01' }
]);
const reposTotal = computed(() => repos.value.length);

const filteredRepos = computed(() => {
  let reposList = repos.value;
  if (searchQuery.value) {
    reposList = reposList.filter(repo => repo.name.includes(searchQuery.value) || repo.description.includes(searchQuery.value));
  }
  if (filterType.value) {
    reposList = reposList.filter(repo => repo.type === filterType.value);
  }
  if (dateRange.value) {
    const [start, end] = dateRange.value;
    reposList = reposList.filter(repo => {
      const createdAt = new Date(repo.created_at!);
      return createdAt >= start && createdAt <= end;
    });
  }
  return reposList.slice((currentPage.value - 1) * pageSize.value, currentPage.value * pageSize.value);
});

const searchRepos = () => {
  currentPage.value = 1;
};

const resetFilters = () => {
  searchQuery.value = '';
  filterType.value = '';
  dateRange.value = null;
  currentPage.value = 1;
};

const openAddEditRepo = (repo: Repo | null = null) => {
  if (repo) {
    form.value = { ...repo };
    selectedRepo.value = repo;
  } else {
    form.value = { name: '', description: '', url: '', type: '' };
    selectedRepo.value = null;
  }
  showAddEditRepo.value = true;
};

const closeAddEditRepo = () => {
  showAddEditRepo.value = false;
};

const saveRepo = () => {
  formRef.value.validate((valid: boolean) => {
    if (valid) {
      const formattedDate = new Date().toLocaleDateString('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
      });
      if (selectedRepo.value) {
        store.commit('updateRepo', { ...form.value, created_at: formattedDate });
      } else {
        form.value.id = Date.now(); // 简单的ID生成策略
        form.value.status = 'active';
        form.value.created_at = formattedDate;
        store.commit('addRepo', form.value);
      }
      closeAddEditRepo();
      ElMessage({
        type: 'success',
        message: selectedRepo.value ? '仓库更新成功!' : '仓库添加成功!',
      });
    } else {
      console.log('验证失败');
      return false;
    }
  });
};

const openRepoDetail = (repo: Repo) => {
  selectedRepo.value = repo;
  showRepoDetail.value = true;
};

const closeRepoDetail = () => {
  showRepoDetail.value = false;
};

const confirmDeleteRepo = (repoId: number) => {
  ElMessageBox.confirm('您确定要删除这个仓库吗？', '确认删除', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning',
  })
    .then(() => {
      store.commit('deleteRepo', repoId);
      ElMessage({
        type: 'success',
        message: '删除成功!',
      });
    })
    .catch(() => {
      ElMessage({
        type: 'info',
        message: '已取消删除',
      });
    });
};

const handleClose = (done: () => void) => {
  ElMessageBox.confirm('您确定要取消该操作吗？')
    .then(() => {
      done();
    })
    .catch(() => {
      // 捕获错误
    });
};

// 图表
const lineOptions = ref({
  padding: [50, 30, 50, 20],
  legend: {
    show: true
  },
  color: ['#00a8ff', '#c23616'],
  data: [
    { '检测日期': 'day1', '项目数': 1, '有缺陷项目': 0 },
    { '检测日期': 'day2', '项目数': 9, '有缺陷项目': 3 },
    { '检测日期': 'day3', '项目数': 5, '有缺陷项目': 1 },
    { '检测日期': 'day4', '项目数': 2, '有缺陷项目': 1 },
    { '检测日期': 'day5', '项目数': 0, '有缺陷项目': 0 },
    { '检测日期': 'day6', '项目数': 3, '有缺陷项目': 3 },
    { '检测日期': 'day7', '项目数': 4, '有缺陷项目': 2 },
    { '检测日期': 'day8', '项目数': 1, '有缺陷项目': 1 },
    { '检测日期': 'day9', '项目数': 1, '有缺陷项目': 0 },
    { '检测日期': 'day10', '项目数': 11, '有缺陷项目': 7 },
    { '检测日期': 'day11', '项目数': 0, '有缺陷项目': 0 },
    { '检测日期': 'day12', '项目数': 7, '有缺陷项目': 2 },
    { '检测日期': 'day13', '项目数': 2, '有缺陷项目': 1 },
    { '检测日期': 'day14', '项目数': 6, '有缺陷项目': 2 }
  ],
  xAxis: {
    data: '检测日期',
    labelRotate: 45
  },
  yAxis: {
    name: '检测次数'
  }
});
const pieOptions = ref({
  type: 'pie',
  legend: {
    show: true,
    position: {
      left: 'center',
      bottom: '10%'
    },
    orient: 'horizontal',
  },
  label: {
    show: true,
    type: 'percent',
    line: true,
  },
  color: ['#c0392b','#e67e22','#ffd32a','#0fbcf9'],
  data: [
    { value: 5, name: '高风险' },
    { value: 7, name: '中风险' },
    { value: 20, name: '低风险' },
    { value: 18, name: '无风险' }
  ]
});

// If using Vuex store, uncomment the following line
// store.dispatch('fetchRepos');

</script>

<style scoped>
.repo-total {
  padding: 10px;
  display: flex;
  flex-direction: column;
  width: 100%;
  border-radius: 8px;
}

.repo-show {
  position: relative;
  display: flex;
  flex-direction: row;
  gap: 20px;
}

.repo-total .repo-data {
  display: flex;
  position: relative;
  flex-direction: row;
  width: 100%;
}

/* this card is inspired form this - https://georgefrancis.dev/ */
.card {
  --border-radius: 0.75rem;
  --primary-color: #7257fa;
  --secondary-color: #3c3852;
  width: 100%;
  font-family: "Arial";
  padding: 1rem;
  cursor: pointer;
  border-radius: var(--border-radius);
  background: #f1f1f3;
  box-shadow: 0px 8px 16px 0px rgb(0 0 0 / 3%);
  position: relative;
}

.card>*+* {
  margin-top: 1.1em;
}

.card .card__content {
  color: var(--secondary-color);
  font-size: 0.86rem;
}

.card .card__title {
  padding: 0;
  font-size: 1.3rem;
  font-weight: bold;
}

.card .card__date {
  color: #6e6b80;
  font-size: 0.8rem;
}

.card .card__arrow {
  position: absolute;
  background: var(--primary-color);
  padding: 0.4rem;
  border-top-left-radius: var(--border-radius);
  border-bottom-right-radius: var(--border-radius);
  bottom: 0;
  right: 0;
  transition: 0.2s;
  display: flex;
  justify-content: center;
  align-items: center;
}

/* hover */
.card:hover .card__title {
  color: var(--primary-color);
  text-decoration: underline;
}

.card:hover .card__arrow {
  background: #111;
}

.title-content {
  width: 100%;
  text-align: center;
  color: #a9a9a9;
  font-size: 16px;
  font-weight: 600;
  margin-top: -15px;
}

.repo-graph {
  align-items: center;
  position: relative;
  margin-top:10px;
  gap: 10px;
  display: flex;
  flex-direction: row;
  width: 100%;
}

.map {
  margin-top: 10px;
  width: 50%;
  border-radius: 10px;
}

.repo-management {
  padding: 10px;
  border-radius: 8px;
}

.repo-total {
  padding: 10px;
}

.header {
  font-size: 20px;
  color: #409eff;
  text-align: center;
  margin-bottom: 20px;
  /* 调整间距 */
}

.info {
  text-align: center;
  color: #606266;
  margin-bottom: 20px;
  /* 调整间距 */
}

.filter-row {
  margin-bottom: 20px;
  background-color: #f8f9fa;
  /* 轻微的背景色增加层次感 */
  padding: 10px;
  border-radius: 8px;
  /* 边角圆润 */
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  /* 添加阴影 */
}

.align-right {
  text-align: right;
}

.el-dialog {
  max-width: 500px;
  /* 限制对话框最大宽度 */
}

.el-dialog__header {
  background-color: #f5f5f5;
  /* 头部背景色 */
  border-bottom: 1px solid #ebeef5;
  /* 头部下边框 */
}

.el-dialog__body {
  padding: 20px;
  /* 内边距 */
}

.el-dialog__footer {
  text-align: right;
}

.el-button {
  transition: background-color 0.3s;
  /* 平滑的背景色过渡 */
}

.el-button:hover {
  background-color: #409eff;
  /* 悬停时改变背景色 */
}

.el-table__row:hover {
  background-color: #f5f5f5;
  /* 表格行悬停效果 */
}
</style>
