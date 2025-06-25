<template>
  <div class="dashboard-container" :class="{'full-screen': isMenuCollapsed}">
    <!-- 全局提示条 -->
    <el-alert
      v-if="useDefaultData"
      title="数据获取失败，当前显示的是默认模拟数据"
      type="warning"
      :closable="false"
      show-icon
      effect="dark"
      class="data-alert"
    />
    
    <!-- 顶部标题区域 -->
    <div class="dashboard-header">
      <div class="dashboard-title">
        <div class="header-controls">
          <el-button type="primary" :icon="Expand" @click="toggleMenu" size="small" class="toggle-btn">
            {{ isMenuCollapsed ? '展开菜单' : '隐藏菜单' }}
          </el-button>
          <el-button type="primary" :icon="RefreshRight" @click="refreshAll" :loading="loading" size="small">刷新</el-button>
        </div>
        <div class="main-title">医疗数据分析平台</div>
        <div class="time">
          {{ currentTime }}
          <div class="date">{{ currentDate }}</div>
        </div>
      </div>
    </div>
    
    <!-- 主要内容区域 -->
    <div class="dashboard-content">
      <!-- 顶部区域 - 2个小图表 -->
      <div class="top-row">
        <div class="chart-box small-chart">
          <BoxplotChart :data="boxplotData" :loading="loading" />
        </div>
        <div class="chart-box small-chart">
          <ScatterBmiChart :data="scatterBmiData" :loading="loading" />
        </div>
      </div>
      
      <!-- 主要内容区域 - 左侧雷达图 + 右侧4个小图表 -->
      <div class="main-content-row">
        <!-- 左侧雷达图 -->
        <div class="left-column">
          <div class="chart-box main-chart">
            <MedicalRadarChart 
              :boxplotData="boxplotData" 
              :scatterBmiData="scatterBmiData" 
              :ageHistData="ageHistData"
              :regionAvgData="regionAvgData"
              :scatterAgeData="scatterAgeData"
              :correlationData="correlationData"
              :loading="loading" 
            />
          </div>
        </div>
        
        <!-- 右侧4个小图表 -->
        <div class="right-column">
          <div class="right-row">
            <div class="chart-box small-chart">
              <AgeHistChart :data="ageHistData" :loading="loading" />
            </div>
            <div class="chart-box small-chart">
              <RegionAvgChart :data="regionAvgData" :loading="loading" />
            </div>
          </div>
          <div class="right-row">
            <div class="chart-box small-chart">
              <ScatterAgeChart :data="scatterAgeData" :loading="loading" />
            </div>
            <div class="chart-box small-chart">
              <CorrelationChart :data="correlationData" :loading="loading" />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, provide } from 'vue';
import { RefreshRight, Expand } from '@element-plus/icons-vue';
import { dashboardApi } from '@/services/api';
import { ElMessage } from 'element-plus';

// 导入图表组件
import BoxplotChart from '@/components/dashboard/BoxplotChart.vue';
import ScatterBmiChart from '@/components/dashboard/ScatterBmiChart.vue';
import AgeHistChart from '@/components/dashboard/AgeHistChart.vue';
import RegionAvgChart from '@/components/dashboard/RegionAvgChart.vue';
import ScatterAgeChart from '@/components/dashboard/ScatterAgeChart.vue';
import CorrelationChart from '@/components/dashboard/CorrelationChart.vue';
import MedicalRadarChart from '@/components/dashboard/MedicalRadarChart.vue';

// 记录是否使用默认数据的标志
const useDefaultData = ref(false);

// 菜单折叠状态
const isMenuCollapsed = ref(false);

// 切换菜单折叠状态
function toggleMenu() {
  isMenuCollapsed.value = !isMenuCollapsed.value;
  
  // 通过自定义事件通知父组件隐藏/显示侧边栏
  const event = new CustomEvent('toggle-sidebar', { 
    detail: { collapsed: isMenuCollapsed.value } 
  });
  window.dispatchEvent(event);
}

// 提供菜单折叠状态给子组件
provide('menuCollapsed', isMenuCollapsed);

// 时间显示
const currentTime = ref('');
const currentDate = ref('');
let timer = null;

function updateDateTime() {
  const now = new Date();
  currentTime.value = now.toLocaleTimeString('zh-CN', { hour12: false });
  currentDate.value = `${now.getFullYear()}年${now.getMonth()+1}月${now.getDate()}日 ${['星期日','星期一','星期二','星期三','星期四','星期五','星期六'][now.getDay()]}`;
}

// 各图表数据
const boxplotData = ref(null);
const scatterBmiData = ref(null);
const ageHistData = ref(null);
const regionAvgData = ref(null);
const scatterAgeData = ref(null);
const correlationData = ref(null);

const loading = ref(false);

// 加载所有数据
async function loadAllData() {
  loading.value = true;
  
  // 重置默认数据标志
  useDefaultData.value = false;
  
  try {
    await Promise.all([
      loadBoxplotData(),
      loadScatterBmiData(),
      loadAgeHistData(),
      loadRegionAvgData(),
      loadScatterAgeData(),
      loadCorrelationData()
    ]);
    
    ElMessage.success('数据加载完成');
  } catch (error) {
    console.error('部分数据加载失败:', error);
    ElMessage.warning('部分数据加载失败，将显示模拟数据');
    useDefaultData.value = true;
  } finally {
    loading.value = false;
  }
}

// 各图表数据加载函数
async function loadBoxplotData() {
  try {
    const response = await dashboardApi.getBoxplotData();
    boxplotData.value = response.data;
  } catch (error) {
    console.error('获取箱线图数据失败:', error);
    // 提供默认数据
    boxplotData.value = {
      'yes': [10000, 15000, 20000, 25000, 30000, 35000, 40000],
      'no': [5000, 8000, 10000, 12000, 15000, 18000, 20000]
    };
    useDefaultData.value = true;
  }
}

async function loadScatterBmiData() {
  try {
    const response = await dashboardApi.getScatterBmiData();
    scatterBmiData.value = response.data;
  } catch (error) {
    console.error('获取BMI散点图数据失败:', error);
    // 提供默认数据
    scatterBmiData.value = [
      [18.5, 8000], [20, 9500], [22, 10200], [24, 11000], 
      [26, 13000], [28, 15000], [30, 18000], [32, 22000], 
      [34, 25000], [36, 28000], [38, 32000], [40, 35000]
    ];
    useDefaultData.value = true;
  }
}

async function loadAgeHistData() {
  try {
    const response = await dashboardApi.getAgeHistData();
    ageHistData.value = response.data;
  } catch (error) {
    console.error('获取年龄直方图数据失败:', error);
    // 提供默认数据
    ageHistData.value = [
      18, 19, 20, 22, 24, 25, 26, 28, 30, 32, 35, 38, 40, 42, 45, 
      48, 50, 52, 55, 58, 60, 62, 64, 24, 28, 32, 35, 38, 42, 45, 
      32, 35, 38, 42, 45, 48, 50, 54, 56, 58, 62, 64, 30, 35, 40, 45, 50, 55, 60
    ];
    useDefaultData.value = true;
  }
}

async function loadRegionAvgData() {
  try {
    const response = await dashboardApi.getRegionAvgData();
    regionAvgData.value = response.data;
  } catch (error) {
    console.error('获取地区平均数据失败:', error);
    // 提供默认数据
    regionAvgData.value = {
      '东北': 12800,
      '华东': 15600,
      '华南': 14200,
      '华中': 13500,
      '华北': 16800,
      '西南': 11800,
      '西北': 10500
    };
    useDefaultData.value = true;
  }
}

async function loadScatterAgeData() {
  try {
    const response = await dashboardApi.getScatterAgeData();
    scatterAgeData.value = response.data;
  } catch (error) {
    console.error('获取年龄散点图数据失败:', error);
    // 提供默认数据
    scatterAgeData.value = [
      [20, 8500, 'no'], [25, 9000, 'no'], [30, 12000, 'no'], [35, 11000, 'no'],
      [40, 15000, 'no'], [45, 14000, 'no'], [50, 17000, 'no'], [55, 19000, 'no'],
      [60, 21000, 'no'], [65, 22000, 'no'], [22, 12500, 'yes'], [27, 16000, 'yes'],
      [32, 20000, 'yes'], [37, 22000, 'yes'], [42, 25000, 'yes'], [47, 28000, 'yes'],
      [52, 32000, 'yes'], [57, 35000, 'yes'], [62, 38000, 'yes']
    ];
    useDefaultData.value = true;
  }
}

async function loadCorrelationData() {
  try {
    const response = await dashboardApi.getCorrelationData();
    correlationData.value = response.data;
  } catch (error) {
    console.error('获取相关性数据失败:', error);
    // 提供默认数据 - 生成一些随机数据进行展示
    const defaultData = [];
    for (let i = 0; i < 50; i++) {
      const age = Math.floor(Math.random() * 40) + 20; // 20-60岁
      const bmi = Math.floor(Math.random() * 25) + 18; // 18-43的BMI
      const children = Math.floor(Math.random() * 5); // 0-4个孩子
      const charges = Math.floor((age * 150) + (bmi * 300) + (children * 2000) + Math.random() * 5000);
      defaultData.push([age, bmi, children, charges]);
    }
    correlationData.value = defaultData;
    useDefaultData.value = true;
  }
}

// 刷新所有图表
function refreshAll() {
  loadAllData();
}

// 生命周期钩子
onMounted(() => {
  loadAllData();
  updateDateTime();
  timer = setInterval(updateDateTime, 1000);
});

onBeforeUnmount(() => {
  clearInterval(timer);
});
</script>

<style scoped>
.dashboard-container {
  width: 100%;
  min-height: 100vh;
  background-color: #061b35;
  background-image: radial-gradient(circle at center, rgba(15, 110, 205, 0.15) 0%, transparent 80%),
                    linear-gradient(to bottom, #041325 0%, #061b35 100%);
  color: #fff;
  padding: 10px;
  position: relative;
  display: flex;
  flex-direction: column;
  overflow-y: auto;
  transition: all 0.3s ease;
}

/* 全屏模式样式 */
.full-screen {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 1000;
  padding: 10px;
  overflow-y: auto;
}

.data-alert {
  margin-bottom: 10px;
}

.dashboard-header {
  height: 60px;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 10px;
}

.dashboard-title {
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
}

.time {
  font-size: 24px;
  color: #00FFFF;
  font-weight: bold;
  text-shadow: 0 0 10px rgba(0, 255, 255, 0.5);
}

.date {
  font-size: 12px;
  color: #7eb6ff;
}

.main-title {
  font-size: 28px;
  font-weight: bold;
  background: linear-gradient(to right, #7eb6ff, #00FFFF);
  -webkit-background-clip: text;
  color: transparent;
  position: relative;
  padding: 0 20px;
  text-shadow: 0 0 15px rgba(0, 255, 255, 0.3);
}

.main-title::before,
.main-title::after {
  content: '';
  position: absolute;
  top: 50%;
  width: 80px;
  height: 1px;
  background: linear-gradient(to right, rgba(126, 182, 255, 0), #7eb6ff);
}

.main-title::before {
  left: -100px;
}

.main-title::after {
  right: -100px;
  transform: rotate(180deg);
}

.header-controls {
  display: flex;
  gap: 10px;
}

.dashboard-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.top-row {
  display: flex;
  gap: 15px;
  height: 180px;
}

.main-content-row {
  flex: 1;
  display: flex;
  gap: 15px;
  min-height: calc(100vh - 280px);
}

.left-column {
  width: 45%;
  display: flex;
  flex-direction: column;
  transition: width 0.3s ease;
}

.right-column {
  width: 55%;
  display: flex;
  flex-direction: column;
  gap: 15px;
  transition: width 0.3s ease;
}

/* 当菜单折叠时的样式 */
.full-screen .left-column {
  width: 40%;
}

.full-screen .right-column {
  width: 60%;
}

.right-row {
  flex: 1;
  display: flex;
  gap: 15px;
}

.right-row:last-child {
  margin-top: -10px; /* 减小上下两行图表之间的间距，原来是-5px */
  padding-bottom: 10px; /* 增加下方图表的高度，原来是5px */
}

.chart-box {
  background-color: rgba(15, 37, 75, 0.7);
  border: 1px solid rgba(15, 110, 205, 0.5);
  border-radius: 6px;
  box-shadow: 0 0 20px rgba(0, 255, 255, 0.15);
  overflow: hidden;
  position: relative;
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
}

.chart-box:hover {
  box-shadow: 0 0 25px rgba(0, 255, 255, 0.25);
  transform: translateY(-2px);
}

.small-chart {
  flex: 1;
}

.main-chart {
  height: 100%;
  width: 100%;
  position: relative;
}

.main-chart::before,
.main-chart::after {
  content: '';
  position: absolute;
  height: 2px;
  background: linear-gradient(to right, transparent, #00FFFF, transparent);
  left: 0;
  right: 0;
  z-index: 1;
}

.main-chart::before {
  top: 0;
}

.main-chart::after {
  bottom: 0;
}

.chart-box::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: linear-gradient(to right, transparent, #00FFFF, transparent);
}

.toggle-btn {
  background-color: rgba(0, 255, 255, 0.2);
  border-color: #00FFFF;
  color: #00FFFF;
}

.toggle-btn:hover {
  background-color: rgba(0, 255, 255, 0.3);
}

.refresh-btn :deep(.el-button) {
  background-color: rgba(0, 255, 255, 0.2);
  border-color: #00FFFF;
  color: #00FFFF;
}

.refresh-btn :deep(.el-button:hover) {
  background-color: rgba(0, 255, 255, 0.3);
}

@media (max-width: 1200px) {
  .main-content-row {
    flex-direction: column;
  }
  
  .left-column,
  .right-column {
    width: 100%;
  }
  
  .left-column {
    min-height: 400px;
  }
}

@media (max-width: 768px) {
  .top-row,
  .right-row {
    flex-direction: column;
    height: auto;
  }
  
  .small-chart {
    min-height: 200px;
  }
  
  .left-column {
    min-height: 350px;
  }
}
</style> 