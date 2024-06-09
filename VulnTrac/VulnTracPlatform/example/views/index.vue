<template>
  <div>
    <full-page :options="options" ref="fullpageRef">
      <div class="section">
        <div class="blurred-wrapper">
          <header class="main-header container">
          </header>
          <section class="hero container">
            <div class="content-wrapper">
              <h5 class="tagline">为个人和团队提供代码脆弱性检测</h5>
              <h1 class="title">
                VulnTrac<span>.</span>
              </h1>
              <p class="message">
                通过提供深入的代码质量和安全解决方案，帮助开发团队发现和修复代码中的脆弱性。深度嵌入到您的开发环境中，确保代码的持续可靠交付。
              </p>
            </div>
          </section>
        </div>
      </div>
      <div class="section">
        <div>
          <div class="wrapper">
            <div class="controls-btn">
              <div class="next-wrapper" @click="nextFun">
                <svg xmlns="http://www.w3.org/2000/svg" style="transform: rotate(180deg);" viewBox="0 0 24 24"
                  width="24" height="24" class="next">
                  <path d="M9 18v-5l8 5V6l-8 5V6H7v12z"></path>
                </svg>
              </div>
              <div class="last-wrapper" @click="lastFun">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24" class="last"
                  :style="{ fill: lastBtnColor }">
                  <path d="M9 18v-5l8 5V6l-8 5V6H7v12z"></path>
                </svg>
              </div>
            </div>
            <div class="describe" :class="describeClass">
              <div class="tips">{{ currentCard.tips }}</div>
              <div class="contnet-text">{{ currentCard.contnetText }}</div>
            </div>
            <div class="card-slide">
              <div v-for="(card, index) in cardStackWrapper" :key="index" :style="cardStyle(card)"
                class="card-stack-wrapper" @mousedown="dragMouseDown($event, index)">
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="section">
        <div class="containerT">
          <div style="font-size: 36px; margin-right: 15px">
            <span>什么群体适合</span><br>
            <span>VulnTrac ？</span>
          </div>
          <div class="class">
          </div>
          <div class="card">
            <div class="imgBx">
              <img src="../assets/img/p1.png" alt="">
            </div>
            <div class="content">
              <h2>计算机初学者</h2>
              <p>
              </p>
            </div>
          </div>
          <div class="card">
            <div class="imgBx">
              <img src="../assets/img/p2.png" alt="">
            </div>
            <div class="content">
              <h2>程序开发人员</h2>
              <p>
              </p>
            </div>
          </div>
          <div class="card">
            <div class="imgBx">
              <img src="../assets/img/p3.png" alt="">
            </div>
            <div class="content">
              <h2>代码审计人员</h2>
              <p>
              </p>
            </div>
          </div>
        </div>
      </div>
      <div class="section">
        <div class="blurred-wrapper">
          <section class="hero container">
            <div class="content-wrapper">
              <h5 class="tagline">为个人和团队提供代码脆弱性检测</h5>
              <h1 class="title">
                VulnTrac<span>.</span>
              </h1>
              <div class="a">
                <div class="b" @click="goToTrialPage"><span>
                    快速开始
                  </span></div>
              </div>
            </div>
          </section>
        </div>
      </div>
    </full-page>
  </div>
</template>
<script setup>
import { ref, onMounted, reactive } from "vue";
import { useRouter } from 'vue-router'
const fullpageRef = ref();
const router = useRouter()
const goToTrialPage = () => {
  router.push('/login')
}
const options = reactive({
  licenseKey: "OPEN-SOURCE-GPLV3-LICENSE",
  navigation: true,
  credits: { enabled: false }
});
const dwellPosition = window.innerWidth
const cardInfo = [
  {
    bgColor: '164,201,216',
    imgUrl: 'example/assets/img/4.png',
    tips: '基于仓库实时监测的全生命周期安全解决方案',
    contnetText: '帮助开发人员自动化持续监控代码库的安全状况，及时发现并弥补安全隐患，从而显著提高代码的可靠性和安全性'
  },
  {
    bgColor: '255,208,213',
    imgUrl: 'example/assets/img/3.png',
    tips: '实现项目级别脆弱性检测的实用工具',
    contnetText: '本产品能够从整体上评估软件系统的安全性，提供了一种全新的安全评估视角，帮助用户全面了解和管理项目安全风险'
  },
  {
    bgColor: '255,208,213',
    imgUrl: 'example/assets/img/2.png',
    tips: '更全面、更强大的代码脆弱性分析工具',
    contnetText: '利用大模型对代码进行更全面的分析，准确识别出潜在的脆弱性，并给出具体修复建议'
  },
  {
    bgColor: '255,208,213',
    imgUrl: 'example/assets/img/1.png',
    tips: '为什么选择 VulnTrac ?',
    contnetText: ''
  }
]

const cardStackWrapper = ref([])
const cardFlagArray = ref([])
const draggedElement = ref(null)
const currentCardIndex = ref(cardInfo.length - 1)
const isDragging = ref(false)

const currentCard = reactive({
  tips: cardInfo[currentCardIndex.value].tips,
  contnetText: cardInfo[currentCardIndex.value].contnetText,
  bgColor: cardInfo[currentCardIndex.value].bgColor,
  imgUrl: cardInfo[currentCardIndex.value].imgUrl
})

const describeClass = ref('describe-appear-animation')

const dragMouseDown = (e, index) => {
  isDragging.value = true
  draggedElement.value = e.target
  e.preventDefault()
  document.onmouseup = closeDragElement
  document.onmousemove = (ev) => elementDrag(ev, index)
}

const elementDrag = (e, index) => {
  e.preventDefault()
  const element = cardStackWrapper.value[index]
  const moveLength = e.clientX - (dwellPosition / 2)
  if (draggedElement.value) {
    draggedElement.value.style.transition = ''
    draggedElement.value.style.transform = `rotateX(0) rotateY(0) rotateZ(${moveLength / dwellPosition * 10}deg) scale(1)`
    draggedElement.value.style.left = `${moveLength}px`
  }
}

const closeDragElement = () => {
  if (draggedElement.value) {
    draggedElement.value.style.transition = '.5s ease'
    document.onmouseup = null
    document.onmousemove = null
    if (Math.abs(parseInt(draggedElement.value.style.left, 10)) > 200) {
      draggedElement.value.style.left = `${parseInt(draggedElement.value.style.left, 10) > 0 ? dwellPosition : -dwellPosition}px`
      moveFun()
    } else {
      draggedElement.value.style.left = "0"
    }
  }
}

const moveFun = () => {
  if (cardStackWrapper.value.length) {
    cardFlagArray.value.unshift(cardStackWrapper.value.pop())
    if (cardStackWrapper.value.length) {
      describeClass.value = 'describe-disappear-animation'
      setTimeout(() => {
        currentCardIndex.value = cardStackWrapper.value.length - 1
        Object.assign(currentCard, cardInfo[currentCardIndex.value])
        describeClass.value = 'describe-appear-animation'
      }, 500)
    } else {
      cardStackWrapper.value = cardFlagArray.value
      cardFlagArray.value = []
      describeClass.value = 'describe-disappear-animation'
      setTimeout(() => {
        currentCardIndex.value = cardStackWrapper.value.length - 1
        Object.assign(currentCard, cardInfo[currentCardIndex.value])
        describeClass.value = 'describe-appear-animation'
      }, 500)
    }
  }
  lastBtnColor()
}

const nextFun = () => {
  const index = cardStackWrapper.value.length - 1
  if (draggedElement.value) {
    draggedElement.value.style.transition = '.5s ease'
    draggedElement.value.style.left = `${dwellPosition}px`
    moveFun()
  }
  lastBtnColor()
}

const lastFun = () => {
  if (cardFlagArray.value.length) {
    cardStackWrapper.value.push(cardFlagArray.value.shift())
    const index = cardStackWrapper.value.length - 1
    if (draggedElement.value) {
      draggedElement.value.style.transition = '.5s ease'
      draggedElement.value.style.left = "0"
    }
    lastBtnColor()
  }
}

const lastBtnColor = () => {
  lastBtnColor.value = cardFlagArray.value.length ? 'rgba(0,0,0,1)' : 'rgba(255,255,255,0.6)'
}

const cardStyle = (card) => ({
  backgroundImage: `url(${card.imgUrl})`,
  transform: `rotateX(5deg) rotateY(0.438122deg) rotateZ(${Math.floor(Math.random() * 9 + 2)}deg) scale(1)`,
  transition: '.5s ease'
})

onMounted(() => {
  cardStackWrapper.value = cardInfo.map(card => reactive({
    ...card,
    style: {
      backgroundImage: `url(${card.imgUrl})`,
      transform: `rotateX(5deg) rotateY(0.438122deg) rotateZ(${Math.floor(Math.random() * 9 + 2)}deg) scale(1)`
    }
  }))
})
</script>

<style lang="less" scoped>
@charset "UTF-8";

@font-face {
  font-family: CircularSpotifyTxTBook;
  font-weight: 700;
  src: url(./asset/font/CircularSpotifyTxT-Book.woff2) format("truetype");
  text-rendering: optimizeLegibility;
}

@font-face {
  font-family: CircularSpotifyTxTBold;
  font-weight: 700;
  src: url(./asset/font/CircularSpotifyTxT-Bold.woff2) format("truetype");
  text-rendering: optimizeLegibility;
}

@font-face {
  font-family: PlastoTrial_ExtraBold;
  font-weight: 700;
  src: url(./asset/font/PlastoTrial-ExtraBold.otf) format("truetype");
  text-rendering: optimizeLegibility;
}

* {
  padding: 0;
  margin: 0;
}

.fp-watermark {
  display: none !important;
}

.logo {
  position: fixed;
  font-family: PlastoTrial_ExtraBold;
  color: black;
  font-size: 50px;
  margin-top: 50px;
}

.wrapper {
  width: 100vw;
  height: 100vh;
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 3.75rem;
  box-sizing: border-box;
  background: url(../assets/img/background.jfif);
  animation: hue 10s infinite alternate;
  overflow: hidden;
}

.wrapper::after {
  content: "";
  width: 100%;
  height: 100%;
  background: inherit;
  position: absolute;
  top: 0;
  left: 0;
  z-index: -1;
  filter: blur(2rem);
  transform: scale(1.15);
}

.wrapper .controls-btn {
  display: flex;
  flex-direction: column-reverse;
}

.wrapper .controls-btn svg {
  margin: 40% 0;
  cursor: pointer;
}

.wrapper .controls-btn .last-wrapper svg {
  fill: rgba(255, 255, 255, 0.6);
}

.card-slide {
  width: calc(20rem + 30vmin);
  height: calc(20rem + 30vmin);
  right: 10%;
  transform: translateX(-10%);
}

.card-slide .card-stack-wrapper {
  width: calc(20rem + 30vmin);
  height: calc(20rem + 30vmin);
  position: absolute;
  left: 0;
  top: 0;
  cursor: grab;
  transform-origin: center center;
  background-color: aqua;
  background-size: cover;
  background-repeat: no-repeat;
}

.card-slide .card-stack-wrapper:last-child {
  transform: rotateX(0) rotateY(0) rotateZ(0) scale(1) !important;
}

.card-slide .card-stack-wrapper .card-stack-inner {
  width: 100%;
  height: 100%;
}

.card-slide .card-stack-wrapper .card-stack-inner img {
  width: 100%;
  height: 100%;
}

.card-slide .card-stack-wrapper:last-child {
  background-color: #000;
  transform: rotateX(0) rotateY(0) rotateZ(0) scale(1);
}

.card-slide .card-stack-wrapper:last-child .card-stack-inner {
  box-shadow: rgba(0, 0, 0, 0) 2px 5px 27px;
}

.describe {
  width: 50%;
  display: flex;
  flex-wrap: wrap;
  margin: 0 5%;
}

.describe .tips {
  font-size: 3rem;
  font-family: CircularSpotifyTxTBold;
  color: white;
  margin-bottom: 10px;
}

.describe .contnet-text {
  font-size: 1.5rem;
  font-family: CircularSpotifyTxTBold;
  color: white;
  cursor: pointer;
}

.describe .contnet-text:hover {
  text-decoration: underline;
}

.card-stack-wrapper-animating-DMD {
  animation: dragMouseDown 0.2s ease-in-out forwards;
}

@keyframes dragMouseDown {
  0% {
    transform: scale(1);
  }

  to {
    transform: scale(1.1);
  }
}

.card-stack-wrapper-animating-DMU {
  animation: dragMouseUp 0.2s ease-in-out forwards;
}

@keyframes dragMouseUp {
  0% {
    transform: scale(1.1);
  }

  to {
    transform: scale(1);
  }
}

.describe-disappear-animation {
  animation: opacityDisappear 0.5s ease-in-out forwards;
}

@keyframes opacityDisappear {
  0% {
    opacity: 1;
  }

  to {
    opacity: 0;
  }
}

.describe-appear-animation {
  animation: opacityAppear 0.5s ease-in-out forwards;
}

@keyframes opacityAppear {
  0% {
    opacity: 0;
  }

  to {
    opacity: 1;
  }
}

@media screen and (max-width: 1024px) {
  .wrapper {
    flex-direction: column;
  }

  .wrapper .controls-btn {
    position: absolute;
    left: 10%;
    top: 50%;
    transform: translate(-10%, -50%);
  }

  .wrapper .card-slide {
    width: calc(20rem + 10vw);
    height: calc(20rem + 10vw);
    transform: translateX(0%);
  }

  .wrapper .card-slide .card-stack-wrapper {
    width: calc(20rem + 10vw);
    height: calc(20rem + 10vw);
  }

  .wrapper .describe {
    margin-bottom: 10%;
  }

  .wrapper .describe .contnet-text {
    font-size: 2rem;
  }
}

* {
  margin: 0;
  padding: 0;
  font-family: "Poppins", sans-serif;
}

body {
  display: flex;
  justify-content: center;
  align-items: center;
  background: #16384c;
}

.containerT {
  position: relative;
  height: 100vh;
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-wrap: wrap;
  padding: 30px;
  background: url(../assets/img/background.jfif) center/cover;
  animation: hue 10s infinite alternate;
  overflow: hidden
}

.containerT::after {
  content: "";
  width: 100%;
  height: 100%;
  background: inherit;
  position: absolute;
  top: 0;
  left: 0;
  z-index: -1;
  filter: blur(2rem);
  transform: scale(1.15);
}

.containerT .card {
  margin-top: 100px;
  position: relative;
  max-width: 300px;
  height: 215px;
  background: #fff;
  margin: 30px 10px;
  padding: 20px 15px;
  display: flex;
  flex-direction: column;
  box-shadow: 0 5px 202px rgba(0, 0, 0, 0.5);
  transition: .3s ease-in-out;
}

.containerT .card:hover {
  height: 420px;
}

.containerT .card .imgBx {
  position: relative;
  width: 260px;
  height: 260px;
  top: -60px;
  left: 20px;
  z-index: 1;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.2);
}

.containerT .card .imgBx img {
  max-width: 100%;
  border-radius: 4px;
}

.containerT .card .content {
  position: relative;
  margin-top: -140px;
  padding: 10px 15px;
  text-align: center;
  color: #111;
  visibility: hidden;
  opacity: 0;
  transition: .3s ease-in-out;
}

.containerT .card:hover .content {
  visibility: visible;
  opacity: 1;
  margin-top: -40px;
  transition-delay: .3s;
}

.blurred-wrapper {
  height: 100vh;
  background: url(../assets/img/background.jfif) center/cover;
  position: relative;
  z-index: 1;
  overflow: hidden;
  animation: hue 10s infinite alternate;
}

.blurred-wrapper::after {
  content: "";
  width: 100%;
  height: 100%;
  background: inherit;
  position: absolute;
  top: 0;
  left: 0;
  z-index: -1;
  filter: blur(2rem);
  transform: scale(1.15);
}

@keyframes hue {
  from {
    filter: hue-rotate(0);
  }

  to {
    filter: hue-rotate(360deg);
  }
}

.main-header {
  height: 12rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.container {
  max-width: 120rem;
  margin: 0 auto;
  padding: 0 1.5rem;
}

.logo {
  color: #fff;
  text-transform: uppercase;
  font-size: 2.5rem;
  font-weight: bold;
}

.btn {
  padding: 1rem 2.5rem;
  border: 2px solid rgba(255, 255, 255, 0.5);
  border-radius: 2.5rem;
  color: #fff;
}

.hero {
  display: flex;
  align-items: center;
  height: calc(100vh - 12rem);
}

.content-wrapper {
  max-width: 40rem;
  transform: translateY(-4rem);
}

.tagline {
  text-transform: uppercase;
  font-size: 1rem;
  font-weight: 100;
  margin-bottom: 1rem;
}

.message {
  font-size: 1.4rem;
  margin-bottom: 3rem;
}

.cta {
  background-color: #000;
}

@media screen and (min-width: 768px) {
  .btn {
    padding: 1.5rem 3rem;
  }

  .content-wrapper {
    max-width: 60rem;
  }

  .tagline {
    font-size: 1.6rem;
  }

  .title {
    font-size: 3rem;
  }

  .message {
    font-size: 2rem;
  }
}

.a {
  position: relative;
  top: 20px;
  width: 200px;
  height: 60px;
  border: solid 10px #fff;
  box-shadow: 0 0 70px rgb(190, 40, 210);
  display: flex;
  justify-content: center;
  align-items: center;
  /* 设置鼠标移上去时变成小手形状 */
  cursor: pointer;
}

.a::after {
  content: '';
  position: fixed;
  width: 200px;
  height: 60px;
  box-shadow: 0 0 5px rgba(190, 40, 210);
  background-color: rgba(100, 30, 225, .4);
}

.a:hover {
  animation: a 1.5s;
}

@keyframes a {

  0%,
  34%,
  68%,
  100% {
    border: solid 10px #fff;
    box-shadow: 0 0 70px rgb(190, 40, 210);
  }

  17%,
  51%,
  85% {
    border: solid 10px rgba(255, 0, 0, .5);
    box-shadow: 0 0 90px rgba(255, 0, 0, .8);
  }
}

.b,
.b::before {
  z-index: 999;
  color: #fff;
  position: absolute;
  font-size: 28px;
  font-weight: 800;
  /* 设置字体间距 */
  letter-spacing: 8px;
}

.b::before {
  content: '快速开始';
  text-shadow: -5px -5px 0px rgb(211, 250, 9), 5px 5px 0px rgb(25, 10, 240);
  /* 使用缩放的方式创建可见显示取余，括号里的四个值分别是top，right，bottom，left */
  clip-path: inset(100% 0px 0px 0px);

}

.a:hover .b::before {
  /* steps设置逐帧动画，值越小越卡顿 */
  animation: move 1.25s steps(2);
}

/* 这是制造混乱的位置和高宽，可以自行改变，随机的 */
@keyframes move {
  0% {
    clip-path: inset(80% 0px 0px 0px);
    transform: translate(-20px, -10px)
  }

  10% {
    clip-path: inset(10% 0px 85% 0px);
    transform: translate(10px, 10px)
  }

  20% {
    clip-path: inset(80% 0px 0px 0px);
    transform: translate(-10px, 10px)
  }

  30% {
    clip-path: inset(10% 0px 85% 0px);
    transform: translate(0px, 5px)
  }

  40% {
    clip-path: inset(50% 0px 30% 0px);
    transform: translate(-5px, 0px)
  }

  50% {
    clip-path: inset(10% 0px 30% 0px);
    transform: translate(5px, 0px)
  }

  60% {
    clip-path: inset(40% 0px 30% 0px);
    transform: translate(5px, 10px)
  }

  70% {
    clip-path: inset(50% 0px 30% 0px);
    transform: translate(-10px, 10px)
  }

  80% {
    clip-path: inset(80% 0px 5% 0px);
    transform: translate(20px, -10px)
  }

  90% {
    clip-path: inset(80% 0px 0px 0px);
    transform: translate(-10px, 0px)
  }

  100% {
    clip-path: inset(80% 0px 0px 0px);
    transform: translate(0px, 0px)
  }
}
</style>