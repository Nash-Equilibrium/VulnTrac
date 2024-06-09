<template>
    <div class="card">
        <div>
            <div class="header">
                VulnTrac<span>.</span>
            </div>
            <div>
                通过提供深入的代码质量和安全解决方案，帮助开发团队发现和修复代码中的脆弱性。深度嵌入到您的开发环境中，确保代码的持续可靠交付。
            </div>
        </div>
    </div>
    <div class="data-map">
        <div class="card data-map-item">
            <div class="header">近14天检测项目数量</div>
            <div>
                <tiny-chart-line :options="lineOptions"></tiny-chart-line>
            </div>
        </div>
        <div class="card data-map-item">
            <div class="header">近14天检测项目情况</div>
            <div>
                <tiny-radar :options="options"></tiny-radar>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { ChartRadar as TinyRadar, ChartLine as TinyChartLine, ChartPie as TinyChartPie } from '@opentiny/vue'

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
})

const options = ref({
  legend: {
    show: true,
    position: {
      left: 'center',
      bottom: 20.1
    }
  },

  // radarMax 用来设置雷达图最外圈的数值
  // 当不设置 radarMax 时， 雷达图坐标系为数据中的最大值
  radarMax: 100,
  data: {
    'Domestic': {
      'Equipment': 41,
      'VM': 91,
      'CSP': 81,
    },
    'Abroad': {
      'Equipment': 72,
      'VM': 55,
      'CSP': 93
    }
  }
})
</script>

<style>
.card {
    align-items: center;
    position: relative;
    margin: 10px;
    background-color: #2C3A47;
    display: fixed;
    flex-direction: column;
    padding: 12px;
    gap: 12px;
    border-radius: 8px;
    cursor: pointer;
}

.card::after {
    content: "";
    z-index: -1;
    position: absolute;
    inset: 0;
    background: linear-gradient(-45deg, #fc00ff 0%, #00dbde 100%);
    filter: blur(10px);
}

.card .header {
    color: #1B9CFC;
    font-size: 24px;
    font-weight: 600;
    margin-bottom: 12px;
}

.card .data-map{
  position: relative;
  display: flex;
  margin-top: -10px;
  margin-bottom: -10px;
}

.card .data-map-item {
  width: 50%;
}
</style>