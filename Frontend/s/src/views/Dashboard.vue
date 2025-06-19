<template>
  <div style="font-size:18px;text-align:center;line-height:1;" class="container">
    <ChartImage :src="chartImg" alt="测试" 
      v-for="i of [1,2,3,4,5]" :key="i"
      style="width:300px;margin:20px">

    </ChartImage>
  </div>
  <!-- 内容超出时会在本区域出现滚动条 -->
</template>

<script setup>
import chartImg from '../assets/logo.png'
import ChartImage from '../components/ChartImage.vue'
</script>

<style scoped>
.dashboard-card {
  border-radius: 18px;
  box-shadow: 0 2px 24px rgba(23, 23, 23, 0.13);
  background: #fff;
  margin-bottom: 28px;
  padding: 48px 0;
}

.container {
  display: flex;
  flex-direction: column;
  flex-wrap: wrap;
  height: 100%;
}
</style>
