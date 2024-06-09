<template>
  <div class="card">
    <div class="header">个人简介</div>
    <div class="user-info">
      <img class="user-avatar" src="../assets/img/1.png" alt="User Avatar">
      <div class="user-details">
        <div>您好，Admin!</div>
        <div>今日晴，20°C - 32°C!</div>
      </div>
    </div>
  </div>
  <div class="card">
    <div class="header">快速链接</div>
    <div class="quick-nav">
      <button class="value">
        <svg viewBox="0 0 16 16" xmlns="http://www.w3.org/2000/svg" data-name="Layer 2">
          <path fill="#7D8590"
            d="m1.5 13v1a.5.5 0 0 0 .3379.4731 18.9718 18.9718 0 0 0 6.1621 1.0269 18.9629 18.9629 0 0 0 6.1621-1.0269.5.5 0 0 0 .3379-.4731v-1a6.5083 6.5083 0 0 0 -4.461-6.1676 3.5 3.5 0 1 0 -4.078 0 6.5083 6.5083 0 0 0 -4.461 6.1676zm4-9a2.5 2.5 0 1 1 2.5 2.5 2.5026 2.5026 0 0 1 -2.5-2.5zm2.5 3.5a5.5066 5.5066 0 0 1 5.5 5.5v.6392a18.08 18.08 0 0 1 -11 0v-.6392a5.5066 5.5066 0 0 1 5.5-5.5z">
          </path>
        </svg>
        关于我们
      </button>
      <button class="value">
        <svg id="Line" viewBox="0 0 32 32" xmlns="http://www.w3.org/2000/svg">
          <path fill="#7D8590" id="XMLID_1646_"
            d="m17.074 30h-2.148c-1.038 0-1.914-.811-1.994-1.846l-.125-1.635c-.687-.208-1.351-.484-1.985-.824l-1.246 1.067c-.788.677-1.98.631-2.715-.104l-1.52-1.52c-.734-.734-.78-1.927-.104-2.715l1.067-1.246c-.34-.635-.616-1.299-.824-1.985l-1.634-.125c-1.035-.079-1.846-.955-1.846-1.993v-2.148c0-1.038.811-1.914 1.846-1.994l1.635-.125c.208-.687.484-1.351.824-1.985l-1.068-1.247c-.676-.788-.631-1.98.104-2.715l1.52-1.52c.734-.734 1.927-.779 2.715-.104l1.246 1.067c.635-.34 1.299-.616 1.985-.824l.125-1.634c.08-1.034.956-1.845 1.994-1.845h2.148c1.038 0 1.914.811 1.994 1.846l.125 1.635c.687.208 1.351.484 1.985.824l1.246-1.067c.787-.676 1.98-.631 2.715.104l1.52 1.52c.734.734.78 1.927.104 2.715l-1.067 1.246c.34.635.616 1.299.824 1.985l1.634.125c1.035.079 1.846.955 1.846 1.993v2.148c0 1.038-.811 1.914-1.846 1.994l-1.635.125c-.208.687-.484 1.351-.824 1.985l1.067 1.246c.677.788.631 1.98-.104 2.715l-1.52 1.52c-.734.734-1.928.78-2.715.104l-1.246-1.067c-.635.34-1.299.616-1.985.824l-.125 1.634c-.079 1.035-.955 1.846-1.993 1.846zm-5.835-6.373c.848.53 1.768.912 2.734 1.135.426.099.739.462.772.898l.18 2.341 2.149-.001.18-2.34c.033-.437.347-.8.772-.898.967-.223 1.887-.604 2.734-1.135.371-.232.849-.197 1.181.089l1.784 1.529 1.52-1.52-1.529-1.784c-.285-.332-.321-.811-.089-1.181.53-.848.912-1.768 1.135-2.734.099-.426.462-.739.898-.772l2.341-.18h-.001v-2.148l-2.34-.18c-.437-.033-.8-.347-.898-.772-.223-.967-.604-1.887-1.135-2.734-.232-.37-.196-.849.089-1.181l1.529-1.784-1.52-1.52-1.784 1.529c-.332.286-.81.321-1.181.089-.848-.53-1.768-.912-2.734-1.135-.426-.099-.739-.462-.772-.898l-.18-2.341-2.148.001-.18 2.34c-.033.437-.347.8-.772.898-.967.223-1.887.604-2.734 1.135-.37.232-.849.197-1.181-.089l-1.785-1.529-1.52 1.52 1.529 1.784c.285.332.321.811.089 1.181-.53.848-.912 1.768-1.135 2.734-.099.426-.462.739-.898.772l-2.341.18.002 2.148 2.34.18c.437.033.8.347.898.772.223.967.604 1.887 1.135 2.734.232.37.196.849-.089 1.181l-1.529 1.784 1.52 1.52 1.784-1.529c.332-.287.813-.32 1.18-.089z">
          </path>
          <path id="XMLID_1645_" fill="#7D8590"
            d="m16 23c-3.859 0-7-3.141-7-7s3.141-7 7-7 7 3.141 7 7-3.141 7-7 7zm0-12c-2.757 0-5 2.243-5 5s2.243 5 5 5 5-2.243 5-5-2.243-5-5-5z">
          </path>
        </svg>
        快速检测
      </button>
      <button class="value">
        <svg viewBox="0 0 128 128" xmlns="http://www.w3.org/2000/svg">
          <path fill="#7D8590"
            d="m109.9 20.63a6.232 6.232 0 0 0 -8.588-.22l-57.463 51.843c-.012.011-.02.024-.031.035s-.023.017-.034.027l-4.721 4.722a1.749 1.749 0 0 0 0 2.475l.341.342-3.16 3.16a8 8 0 0 0 -1.424 1.967 11.382 11.382 0 0 0 -12.055 10.609c-.006.036-.011.074-.015.111a5.763 5.763 0 0 1 -4.928 5.41 1.75 1.75 0 0 0 -.844 3.14c4.844 3.619 9.4 4.915 13.338 4.915a17.14 17.14 0 0 0 11.738-4.545l.182-.167a11.354 11.354 0 0 0 3.348-8.081c0-.225-.02-.445-.032-.667a8.041 8.041 0 0 0 1.962-1.421l3.16-3.161.342.342a1.749 1.749 0 0 0 2.475 0l4.722-4.722c.011-.011.018-.025.029-.036s.023-.018.033-.029l51.844-57.46a6.236 6.236 0 0 0 -.219-8.589zm-70.1 81.311-.122.111c-.808.787-7.667 6.974-17.826 1.221a9.166 9.166 0 0 0 4.36-7.036 1.758 1.758 0 0 0 .036-.273 7.892 7.892 0 0 1 9.122-7.414c.017.005.031.014.048.019a1.717 1.717 0 0 0 .379.055 7.918 7.918 0 0 1 4 13.317zm5.239-10.131c-.093.093-.194.176-.293.26a11.459 11.459 0 0 0 -6.289-6.286c.084-.1.167-.2.261-.3l3.161-3.161 6.321 6.326zm7.214-4.057-9.479-9.479 2.247-2.247 9.479 9.479zm55.267-60.879-50.61 56.092-9.348-9.348 56.092-50.61a2.737 2.737 0 0 1 3.866 3.866z">
          </path>
        </svg>
        检测记录
      </button>
      <button class="value">
        <svg id="svg8" viewBox="0 0 32 32" xmlns="http://www.w3.org/2000/svg">
          <g id="layer1" transform="translate(-33.022 -30.617)">
            <path fill="#7D8590" id="path26276"
              d="m49.021 31.617c-2.673 0-4.861 2.188-4.861 4.861 0 1.606.798 3.081 1.873 3.834h-7.896c-1.7 0-3.098 1.401-3.098 3.1s1.399 3.098 3.098 3.098h4.377l.223 2.641s-1.764 8.565-1.764 8.566c-.438 1.642.55 3.355 2.191 3.795s3.327-.494 3.799-2.191l2.059-5.189 2.059 5.189c.44 1.643 2.157 2.631 3.799 2.191s2.63-2.153 2.191-3.795l-1.764-8.566.223-2.641h4.377c1.699 0 3.098-1.399 3.098-3.098s-1.397-3.1-3.098-3.1h-7.928c1.102-.771 1.904-2.228 1.904-3.834 0-2.672-2.189-4.861-4.862-4.861zm0 2c1.592 0 2.861 1.27 2.861 2.861 0 1.169-.705 2.214-1.789 2.652-.501.203-.75.767-.563 1.273l.463 1.254c.145.393.519.654.938.654h8.975c.626 0 1.098.473 1.098 1.1s-.471 1.098-1.098 1.098h-5.297c-.52 0-.952.398-.996.916l-.311 3.701c-.008.096-.002.191.018.285 0 0 1.813 8.802 1.816 8.82.162.604-.173 1.186-.777 1.348s-1.184-.173-1.346-.777c-.01-.037-3.063-7.76-3.063-7.76-.334-.842-1.525-.842-1.859 0 0 0-3.052 7.723-3.063 7.76-.162.604-.741.939-1.346.777s-.939-.743-.777-1.348c.004-.019 1.816-8.82 1.816-8.82.02-.094.025-.189.018-.285l-.311-3.701c-.044-.518-.477-.916-.996-.916h-5.297c-.627 0-1.098-.471-1.098-1.098s.472-1.1 1.098-1.1h8.975c.419 0 .793-.262.938-.654l.463-1.254c.188-.507-.062-1.07-.563-1.273-1.084-.438-1.789-1.483-1.789-2.652.001-1.591 1.271-2.861 2.862-2.861z">
            </path>
          </g>
        </svg>
        仓库管理
      </button>
      <button class="value">
        <svg fill="none" viewBox="0 0 24 25" xmlns="http://www.w3.org/2000/svg">
          <path clip-rule="evenodd"
            d="m11.9572 4.31201c-3.35401 0-6.00906 2.59741-6.00906 5.67742v3.29037c0 .1986-.05916.3927-.16992.5576l-1.62529 2.4193-.01077.0157c-.18701.2673-.16653.5113-.07001.6868.10031.1825.31959.3528.67282.3528h14.52603c.2546 0 .5013-.1515.6391-.3968.1315-.2343.1117-.4475-.0118-.6093-.0065-.0085-.0129-.0171-.0191-.0258l-1.7269-2.4194c-.121-.1695-.186-.3726-.186-.5809v-3.29037c0-1.54561-.6851-3.023-1.7072-4.00431-1.1617-1.01594-2.6545-1.67311-4.3019-1.67311zm-8.00906 5.67742c0-4.27483 3.64294-7.67742 8.00906-7.67742 2.2055 0 4.1606.88547 5.6378 2.18455.01.00877.0198.01774.0294.02691 1.408 1.34136 2.3419 3.34131 2.3419 5.46596v2.97007l1.5325 2.1471c.6775.8999.6054 1.9859.1552 2.7877-.4464.795-1.3171 1.4177-2.383 1.4177h-14.52603c-2.16218 0-3.55087-2.302-2.24739-4.1777l1.45056-2.1593zm4.05187 11.32257c0-.5523.44772-1 1-1h5.99999c.5523 0 1 .4477 1 1s-.4477 1-1 1h-5.99999c-.55228 0-1-.4477-1-1z"
            fill="#7D8590" fill-rule="evenodd"></path>
        </svg>
        仓库历史
      </button>
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
        <tiny-chart-pie :color-mode="pieColor" :options="pieOptions"></tiny-chart-pie>
      </div>
    </div>
  </div>
  <div class="card">
    <div class="header">检测历史</div>
    <div class="project-section">
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
                    <path d="M16.172 11l-5.364-5.364 1.414-1.414L20 12l-7.778 7.778-1.414-1.414L16.172 13H4v-2z"
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
  </div>
  <div class="card"></div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import { ChartLine as TinyChartLine, ChartPie as TinyChartPie } from '@opentiny/vue'

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
    color: 'white'
  },
  color: ['#c0392b','#e67e22','#ffd32a','#0fbcf9'],
  data: [
    { value: 5, name: '高风险' },
    { value: 7, name: '中风险' },
    { value: 20, name: '低风险' },
    { value: 18, name: '无风险' }
  ]
})

</script>

<style scoped>
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
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 12px;
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

.quick-nav {
  display: flex;
  flex-direction: row;
  width: 100%;
  background-color: #0d1117;
  justify-content: center;
  border-radius: 5px;
  border: 2px solid;
  border-color: #12CBC4;
  padding: 10px;
  background-color: #2C3A47;
}

.quick-nav .value {
  background-color: transparent;
  border: none;
  padding: 10px;
  color: white;
  display: flex;
  gap: 5px;
  cursor: pointer;
  border-radius: 4px;
  margin: 0 10px 0 10px;
  width: 20%;
  height: auto;
}

.quick-nav .value:not(:active):hover,
.quick-nav .value:focus {
  background-color: #21262c;
}

.quick-nav .value:focus,
.quick-nav .value:active {
  background-color: #1a1f24;
  outline: none;
}

.quick-nav .value::before {
  content: "";
  position: absolute;
  top: 5px;
  left: -10px;
  width: 5px;
  height: 80%;
  background-color: #2f81f7;
  border-radius: 5px;
  opacity: 0;
}

.quick-nav .value:focus::before,
.quick-nav .value:active::before {
  opacity: 1;
}

.quick-nav .value svg {
  width: 15px;
}

.project-section {
  position: relative;
  width: 100%;
}

.project-grid {
  display: flex;
  justify-content: first;
  gap: 20px;
}

.project-item {
  width: 33%;
  height: 150px;
}

.project-card {
  position: relative;
  width: auto;
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

.data-map{
  position: relative;
  display: flex;
  margin-top: -10px;
  margin-bottom: -10px;
}

.data-map-item {
  width: 50%;
}
</style>