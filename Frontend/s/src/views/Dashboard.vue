<template>
  <div style="font-size:18px;text-align:center;line-height:1;" class="container">
    <ChartImage :src="i.img" :alt="i.txt"
      v-for="i of arr" :key="i.txt"
      style="width:300px;margin:20px">

    </ChartImage>
  </div>
</template>

<script setup>
import { readonly } from 'vue'

import ChartImage from '../components/ChartImage.vue'

import ROC from '../assets/ROC.png'
import SmokeAge from '../assets/吸烟年龄统计图.png'
import AgeVisual from '../assets/年龄可视化.png'
import AgeCount from '../assets/患者年龄统计.png'
import PatientsCount from '../assets/患者统计.png'
import Matrix from '../assets/混淆矩阵.png'
import HeatMap from '../assets/特征热力图.png'
import PatientsCompare from '../assets/肺癌患者数量对比.png'

const arr = readonly([
  {
    img: ROC,
    txt: 'ROC预测曲线',
  },
  {
    img: SmokeAge,
    txt: '吸烟年龄统计图',
  },
  {
    img: AgeVisual,
    txt: '年龄相关可视化',
  },
  {
    img: AgeCount,
    txt: '患者年龄统计',
  },
  {
    img: PatientsCount,
    txt: '患者数量统计',
  },
  {
    img: Matrix,
    txt: '混淆矩阵',
  },
  {
    img: HeatMap,
    txt: '特征热力图',
  },
  {
    img: PatientsCompare,
    txt: '肺癌患者数量对比',
  },
])
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
  overflow: scroll;
}
</style>
