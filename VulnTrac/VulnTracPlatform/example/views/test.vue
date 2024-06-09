<template>
	<div class="user-center-card">
		<el-divider style="margin-bottom: 20px;"></el-divider>
		<div class="user-info">
			<img class="user-avatar" src="../assets/img/1.png" alt="User Avatar">
			<div class="user-details">
				<div tag="b" size="large">您好，Admin!</div>
				<div size="small">今日晴，20°C - 32°C!</div>
			</div>
		</div>

		<el-divider style="margin-bottom: 20px;"></el-divider>

		<div class="quick-nav">
			<div class="nav-item" v-for="item in quickNavItems" :key="item.label">
				<el-link :underline="false" :href="item.link">
					<el-icon :name="item.icon"></el-icon>
					<div>{{ item.label }}</div>
				</el-link>
			</div>
		</div>

		<el-divider style="margin-bottom: 5px;"></el-divider>

		<div class="project-section">
			<el-text style="color: #1B9CFC;margin-bottom: 20px" tag="b" size="large">代码漏洞检测项目</el-text>
			<div style="margin-top: 15px" class="project-grid">
				<div class="project-item" v-for="project in projects" :key="project.name">
					<article class="project-card">
						<div class="temporary_text">
							{{ project.name }}
						</div>
						<div class="card_content">
							<span class="card_title">{{ project.name }}</span>
							<span class="card_subtitle">{{ project.date }}</span>
							<p class="card_description">
							<div>{{ project.description }}</div>

							<button class="cssbuttons-io-button" @click="">
								<div class="icon">
									<svg height="24" width="24" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
										<path d="M0 0h24v24H0z" fill="none"></path>
										<path
											d="M16.172 11l-5.364-5.364 1.414-1.414L20 12l-7.778 7.778-1.414-1.414L16.172 13H4v-2z"
											fill="currentColor"></path>
									</svg>
								</div>
							</button>
							</p>
						</div>
					</article>
				</div>
			</div>
		</div>

		<el-divider></el-divider>

		<div class="recent-activity">
			<el-row :gutter="25">
				<el-col :span="11" class="chart">
					<el-card>
						<template #header>
							<el-text tag="b" style="" size="large">近14天检测项目数</el-text>
						</template>
						<div>
							<tiny-chart-line :options="lineOptions"></tiny-chart-line>
						</div>
					</el-card>
				</el-col>
				<el-col :span="1">
				</el-col>
				<el-col :span="11" class="chart">
					<el-card>
						<template #header>
							<el-text tag="b" size="large">近14天项目分析</el-text>
						</template>
						<div>
							<tiny-chart-pie :options="pieOptions"></tiny-chart-pie>
						</div>
					</el-card>
				</el-col>
			</el-row>
		</div>
	</div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import { ChartLine as TinyChartLine, ChartPie as TinyChartPie } from '@opentiny/vue'
const quickNavItems = ref([
	{ label: '关于我们', icon: 'home', link: '/' },
	{ label: '开始检测', icon: 'search', link: '/start' },
	{ label: '检测记录', icon: 'document', link: '/pages/history' },
	{ label: '检测管理', icon: 'settings', link: '/pages/setup' },
	{ label: '仓库管理', icon: 'lock', link: '/repos/setup' },
	{ label: '监测记录', icon: 'file', link: '/repos/history' }
])

const projects = ref([
	{ name: '项目1', description: '描述1', icon: 'folder', date: '2024-06-01' },
	{ name: '项目2', description: '描述2', icon: 'folder', date: '2024-06-02' },
	{ name: '项目3', description: '描述3', icon: 'folder', date: '2024-06-03' },
	{ name: '项目4', description: '描述4', icon: 'folder', date: '2024-06-04' },
	{ name: '项目5', description: '描述5', icon: 'folder', date: '2024-06-05' },
	{ name: '项目6', description: '描述6', icon: 'folder', date: '2024-06-06' }
])

const lineOptions = ref({
	padding: [50, 30, 50, 20],
	legend: {
		show: true
	},
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
})

const pieOptions = ref({
	type: 'pie',
	legend: {
		show: true,
		position: {
			left: 'center',
			bottom: '10%'
		},
		orient: 'horizontal',

		itemHeight: 20,

		itemWidth: 20
	},
	label: {
		show: true,
		type: 'percent',
		line: true
	},
	data: [
		{ value: 5, name: '高风险' },
		{ value: 7, name: '中风险' },
		{ value: 20, name: '低风险' },
		{ value: 18, name: '无风险' }
	]
})
</script>

<style scoped>
.user-center-card {
	align-items: center;
	position: relative;
	margin: 2.5%;
	background-color: #2C3A47;
	display: fixed;
	flex-direction: column;
	padding: 12px;
	gap: 12px;
	border-radius: 8px;
	cursor: pointer;
}

.user-center-card::after {
	content: "";
	z-index: -1;
	position: absolute;
	inset: 0;
	background: linear-gradient(-45deg, #fc00ff 0%, #00dbde 100%);
	filter: blur(10px);
}

.user-center-card {
	padding: 20px;
	border-radius: 8px;
}

.user-info {
	display: flex;
	align-items: center;
	gap: 20px;
}

.user-avatar {
	width: 80px;
	height: 80px;
	border-radius: 50%;
}

.user-details {
	display: flex;
	flex-direction: column;
}

.user-stats {
	display: flex;
	justify-content: space-around;
	margin: 20px 0;
}

.stat-item {
	text-align: center;
}

.quick-nav {
	display: flex;
	flex-wrap: wrap;
	gap: 20px;
	justify-content: space-between;
}

.nav-item {
	width: 30%;
	text-align: center;
}

.nav-item el-icon {
	font-size: 24px;
	margin-bottom: 10px;
}

.project-section {
	margin-top: 20px;
	position: relative;
	width: 100%;
}

.project-grid {
	display: flex;
	flex-wrap: wrap;
	gap: 20px;
}

.project-item {
	width: 30%;
	height: 150px;
}

.project-card {
	position: relative;
	width: 100%;
	height: 100%;
	color: #2e2d31;
	overflow: hidden;
	border-radius: 20px;
	border: 2px solid #b5bfd9;
}

.project-card .temporary_text {
	font-weight: bold;
	font-size: 24px;
	padding: 6px 12px;
	color: #12CBC4;
}

.project-card .card_title {
	font-weight: bold;
}

.project-card .card_content {
	position: absolute;
	left: 0;
	bottom: 0;
	/* edit the width to fit card */
	width: 100%;
	padding: 20px;
	background: #12CBC4;
	border-top-left-radius: 20px;
	/* edit here to change the height of the content box */
	transform: translateY(50%);
	transition: transform .25s;
}

.project-card .card_content::before {
	content: '';
	position: absolute;
	top: -47px;
	right: -45px;
	width: 100px;
	height: 100px;
	transform: rotate(-175deg);
	border-radius: 50%;
	box-shadow: inset 48px 48px #12CBC4;
}

.project-card .card_title {
	color: #131313;
	line-height: 15px;
}

.project-card .card_subtitle {
	display: block;
	font-size: 12px;
	margin-bottom: 10px;
}

.project-card .card_description {
	font-size: 14px;
	opacity: 0;
	transition: opacity .5s;
	display: flex;
	justify-content: space-between;
}

.project-card:hover .card_content {
	transform: translateY(0);
}

.project-card:hover .card_description {
	opacity: 1;
	transition-delay: .25s;
}

.cssbuttons-io-button {
  background: #12CBC4;
  color: white;
  font-family: inherit;
  font-size: 10px;
  font-weight: 500;
  border-radius: 0.9em;
  border: none;
  letter-spacing: 0.05em;
  display: flex;
  align-items: center;
  overflow: hidden;
  position: relative;
  height: 2.8em;
  padding-right: 3.3em;
  cursor: pointer;
  justify-self: end;
}

.cssbuttons-io-button .icon {
  background: white;
  margin-left: 1em;
  position: absolute;
  display: flex;
  align-items: center;
  justify-content: center;
  height: 2.2em;
  width: 2.2em;
  border-radius: 0.7em;
  box-shadow: 0.1em 0.1em 0.6em 0.2em #12CBC4;
  right: 0.3em;
  transition: all 0.3s;
}

.cssbuttons-io-button:hover .icon {
  width: calc(100% - 0.6em);
}

.cssbuttons-io-button .icon svg {
  width: 1.1em;
  transition: transform 0.3s;
  color: #7b52b9;
}

.cssbuttons-io-button:hover .icon svg {
  transform: translateX(0.1em);
}

.cssbuttons-io-button:active .icon {
  transform: scale(0.95);
}


.recent-activity {
	margin-top: 20px;
}

.activity-list {
	display: flex;
	flex-direction: column;
	gap: 20px;
}

.activity-item {
	display: flex;
	align-items: center;
	gap: 10px;
}

.activity-details {
	display: flex;
	flex-direction: column;
}
</style>