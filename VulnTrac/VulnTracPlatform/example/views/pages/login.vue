<template>
    <div class="blurred-wrapper">
        <mi-login :action="/v1/login" />
    </div>
</template>

<!-- <script setup lang="ts">
const handleLogin = () => {
    console.log('login')
    // do sometion
    // return `boolean` or `string`
    return true
}
</script> -->

<style>
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
</style>