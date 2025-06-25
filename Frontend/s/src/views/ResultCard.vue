<template>
  <el-card class="result-card" shadow="hover">
    <div class="result-header" :class="resultClass">
      <el-icon :size="36">
        <CircleCheck v-if="prediction === 0" />
        <WarningFilled v-else />
      </el-icon>
      <span class="result-label">
        {{ predictionLabel }}
      </span>
    </div>
    <div class="result-probability">
      <el-progress
        :percentage="probabilityPercent"
        :color="probabilityColor"
        :stroke-width="18"
        status="error"
        :text-inside="true"
      >
      </el-progress>
      <span class="probability-text">
        患病概率：{{ probabilityPercent }}%
      </span>
    </div>
    <div>
      <slot>
      <!-- 放入图片 -->
      </slot>
    </div>
  </el-card>
</template>

<script setup>
import { computed } from 'vue'
import { CircleCheck, WarningFilled } from '@element-plus/icons-vue'

const props = defineProps({
  prediction: {
    type: Number,
    required: true
  },
  predictionLabel: {
    type: String,
    required: true
  },
  probability: {
    type: Number, // 0~1
    required: true
  }
})

const probabilityPercent = computed(() => Math.round(props.probability * 100))

const resultClass = computed(() =>
  props.prediction === 0 ? 'non-cancer' : 'cancer'
)

const probabilityColor = computed(() =>
  props.prediction === 0 ? '#67C23A' : '#F56C6C'
)
</script>

<style scoped>
.result-card {
  max-width: 400px;
  margin: 0 auto;
  padding: 32px 28px;
  border-radius: 20px;
  box-shadow: 0 8px 32px 0 rgba(60, 80, 120, 0.08);
  background: linear-gradient(120deg, #f0f9ff 0%, #eaf6ff 100%);
  border: none;
}
.result-header {
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.8rem;
  font-weight: bold;
  margin-bottom: 24px;
  gap: 12px;
}
.result-header.cancer {
  color: #F56C6C;
}
.result-header.non-cancer {
  color: #67C23A;
}
.result-probability {
  margin-top: 12px;
  display: flex;
  flex-direction: column;
  align-items: center;
}
.probability-text {
  margin-top: 10px;
  font-size: 1.15rem;
  color: #333;
}
</style>
