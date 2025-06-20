<template>
    <div class="chart-image-wrapper">
        <el-card style="width: 320px" shadow="hover">
            <template v-slot:header>
                {{ alt }}
            </template>
            <img v-if="src" :src="src" class="chart-img" :alt="alt" @error="onError"
              @mousedown="down" @mouseup="up" />
            <div v-else class="placeholder">暂无统计图</div>
        </el-card>
    </div>
</template>

<script setup>
import { ref } from 'vue'
// eslint-disable-next-line no-undef, no-unused-vars
const props = defineProps({
  src: { type: String, required: false, default: '' },
  alt: { type: String, required: false, default: '统计图' }
})


const hasError = ref(false)

function onError() {
  hasError.value = true
}

function down() {
  
}

function up() {
  
}

</script>

<style scoped>
.chart-image-wrapper {
  width: 100%;
  align-items: center;
  /* min-height: 320px; */
  margin: 20px;
}
.chart-card {
  width: 300px;
  border-radius: 18px;
  box-shadow: 0 2px 24px rgba(64,158,255,0.13);
  background: #fff;
  align-items: center;
  min-height: 280px;
  padding: 28px 0;
}
.chart-img {
  max-width: 100%;
  max-height: 400px;
  object-fit: contain;
  display: block;
  margin: 0 auto;
  border-radius: 10px;
  background: #f2f6fc;
  transition: box-shadow 0.3s;
  box-shadow: 0 1px 8px rgba(80, 120, 255, 0.10);
}
.placeholder {
  font-size: 18px;
  color: #b0b0b0;
  text-align: center;
  width: 100%;
  height: 180px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f8fafc;
  border-radius: 12px;
}
</style>
