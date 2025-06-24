<template>
  <el-card class="upload-card">
    <div class="title">脑肿瘤类型识别</div>
    <el-upload
      class="upload-demo"
      drag
      action=""
      :auto-upload="false"
      :before-upload="beforeUpload"
      :on-change="handleChange"
      :file-list="fileList"
      accept="image/*"
    >
      <i class="el-icon-upload"></i>
      <div class="el-upload__text">拖拽或点击上传脑部影像</div>
    </el-upload>
    <el-button
      class="upload-btn"
      type="primary"
      :disabled="fileList.length===0 || loading"
      @click="handleSubmit"
    >识别肿瘤类型</el-button>
    <div v-if="loading" class="loading">正在识别，请稍候...</div>
    <result-view v-if="result.prediction" v-bind="result" />
  </el-card>
</template>
    <!-- :probability="result.probability" :prediction="result.prediction" :prediction-label="result.predictedLabel" -->

<script setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import ResultView from './ResultCard.vue'
import { PredictTumor } from '@/api/ml'

const fileList = ref([])
const loading = ref(false)
const result = ref({
        prediction: null,
        probability: null,
        predictionLabel: null
      })

function beforeUpload() {
  // 阻止 el-upload 自动上
  return false
}

function handleChange(file) {
  fileList.value = [file];
}

async function handleSubmit() {
  if (!fileList.value.length) return
  loading.value = true
  try {
    const formData = new FormData()
    formData.append('image', fileList.value[0].raw)
    const res = (await PredictTumor(formData)).data
    console.log(res);
    result.value = {
      prediction: res.predicted_label,
      probability: res.probability[res.predicted_label],
      predictionLabel: res.predicted_label
    }
  } catch (e) {
    result.value = {};
    ElMessage.error('识别失败，请重试')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.upload-card {
  max-width: 420px;
  margin: 40px auto;
  padding: 24px 20px;
  border-radius: 18px;
  box-shadow: 0 6px 24px #0001;
}
.title {
  font-size: 1.25rem;
  font-weight: 600;
  text-align: center;
  margin-bottom: 18px;
  letter-spacing: 2px;
}
.upload-demo {
  margin-bottom: 12px;
}
.upload-btn {
  width: 100%;
  margin-bottom: 16px;
}
.loading {
  text-align: center;
  color: #409EFF;
  margin-bottom: 16px;
}
</style>
