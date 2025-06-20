<template>
  <div class="dashboard-container">
    <div class="dashboard-header">
      <h2 class="dashboard-title">肺癌预测数据可视化分析</h2>
      <p class="dashboard-description">该系统基于多维度数据分析，展示肺癌与各种因素的相关性，包括年龄、性别、吸烟习惯等，帮助医生和研究人员更好地理解肺癌发病规律。</p>
      <div class="header-stats">
        <div class="stat-item">
          <div class="stat-value">309</div>
          <div class="stat-label">总样本数</div>
        </div>
        <div class="stat-item">
          <div class="stat-value">270</div>
          <div class="stat-label">肺癌样本</div>
        </div>
        <div class="stat-item">
          <div class="stat-value">39</div>
          <div class="stat-label">非肺癌样本</div>
        </div>
        <div class="stat-item">
          <div class="stat-value">87.4%</div>
          <div class="stat-label">肺癌比例</div>
        </div>
      </div>
    </div>
    
    <div class="content-panel">
      <div class="chart-wrapper">
        <div v-if="currentView === 'age'" class="chart-container">
          <age-distribution-chart />
        </div>
        
        <div v-else-if="currentView === 'gender'" class="chart-container">
          <gender-cancer-chart />
        </div>
        
        <div v-else-if="currentView === 'correlation'" class="chart-container">
          <correlation-matrix-chart />
        </div>
        
        <div v-else-if="currentView === 'smoking'" class="chart-container">
          <smoking-stats-chart />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import AgeDistributionChart from '../components/charts/AgeDistributionChart.vue'
import GenderCancerChart from '../components/charts/GenderCancerChart.vue'
import CorrelationMatrixChart from '../components/charts/CorrelationMatrixChart.vue'
import SmokingStatsChart from '../components/charts/SmokingStatsChart.vue'

const route = useRoute()

// 根据当前路由确定要显示的视图
const currentView = computed(() => {
  const path = route.path
  if (path.includes('gender')) return 'gender'
  if (path.includes('correlation')) return 'correlation'
  if (path.includes('smoking')) return 'smoking'
  return 'age' // 默认显示年龄分析
})

// 监听路由变化
watch(() => route.path, (newPath) => {
  console.log('路由变化:', newPath)
})

onMounted(() => {
  console.log('Dashboard组件已加载，当前视图:', currentView.value)
})
</script>

<style scoped>
.dashboard-container {
  width: 100%;
  height: 100%;
  padding: 20px 20px 0 20px; /* 移除底部内边距 */
  box-sizing: border-box;
  overflow-y: auto; /* 使整个容器可滚动 */
  background-color: #f5f7fa;
  background-image: linear-gradient(135deg, #f5f7fa 0%, #f0f4f8 100%);
  display: flex;
  flex-direction: column;
}

.dashboard-header {
  width: 100%;
  margin-bottom: 24px;
  background: #fff;
  padding: 25px 30px;
  border-radius: 12px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
  position: relative;
  overflow: visible;
  flex-shrink: 0; /* 防止头部被压缩 */
}

.dashboard-header::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 4px;
  background: linear-gradient(90deg, #409EFF, #53a8ff, #66b1ff);
}

.dashboard-title {
  margin: 0;
  font-size: 28px;
  color: #303133;
  margin-bottom: 12px;
  font-weight: 600;
}

.dashboard-description {
  margin: 0;
  color: #606266;
  line-height: 1.8;
  font-size: 15px;
  max-width: 100%;
  margin-bottom: 20px;
}

.header-stats {
  display: flex;
  margin-top: 24px;
  background-color: #f8fbff;
  border-radius: 8px;
  padding: 16px;
  justify-content: space-between;
  flex-wrap: wrap;
}

.stat-item {
  text-align: center;
  flex: 1;
  min-width: 120px;
  padding: 0 15px;
  margin-bottom: 10px;
  border-right: 1px solid #e6ebf5;
}

.stat-item:last-child {
  border-right: none;
}

.stat-value {
  font-size: 24px;
  font-weight: bold;
  color: #409EFF;
  line-height: 1.2;
  margin-bottom: 6px;
}

.stat-label {
  font-size: 14px;
  color: #606266;
}

.content-panel {
  width: 100%;
  background: #fff;
  border-radius: 12px 12px 0 0; /* 移除底部圆角 */
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
  padding: 24px;
  margin-bottom: 0; /* 移除底部外边距 */
  flex: 1; /* 占据剩余空间 */
  display: flex;
  flex-direction: column;
}

.chart-wrapper {
  width: 100%;
  flex: 1; /* 占据内容区域的所有剩余空间 */
  display: flex;
  flex-direction: column;
}

.chart-container {
  width: 100%;
  flex: 1; /* 占据图表包装器的所有剩余空间 */
  padding: 10px 0;
  min-height: 500px; /* 确保图表有足够的高度 */
}

@media (max-width: 768px) {
  .header-stats {
    flex-direction: column;
    align-items: center;
  }
  
  .stat-item {
    width: 100%;
    margin-bottom: 15px;
    border-right: none;
    border-bottom: 1px solid #e6ebf5;
    padding-bottom: 15px;
  }
  
  .stat-item:last-child {
    border-bottom: none;
    margin-bottom: 0;
  }
}
</style>
