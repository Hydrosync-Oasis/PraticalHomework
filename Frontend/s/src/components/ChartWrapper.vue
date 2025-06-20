<template>
  <div class="chart-container">
    <div class="chart-header">
      <div class="chart-title-area">
        <div class="chart-title" v-if="title">{{ title }}</div>
        <div class="chart-subtitle" v-if="subtitle">{{ subtitle }}</div>
      </div>
    </div>

    <div class="chart-intro" v-if="intro">
      <div class="intro-icon"><el-icon><InfoFilled /></el-icon></div>
      <div class="intro-text">{{ intro }}</div>
    </div>

    <div class="chart-loading" v-if="loading">
      <el-icon class="is-loading"><Loading /></el-icon>
      <span>加载中...</span>
    </div>
    <div class="chart-error" v-else-if="error || internalError">
      <el-icon><WarningFilled /></el-icon>
      <span>{{ error ? errorMessage : internalErrorMessage || '图表加载失败' }}</span>
      <el-button type="primary" size="small" @click="retryChart" style="margin-top:10px">
        重试
      </el-button>
    </div>
    <div class="chart-empty" v-else-if="isEmpty">
      <el-empty description="暂无数据"></el-empty>
    </div>
    <div class="chart-content" v-else :style="{height: height}">
      <v-chart 
        v-if="isReady && !isEmpty && !error && !internalError && !loading"
        class="chart" 
        :option="safeOption" 
        :autoresize="true"
        :theme="theme"
        @click="handleChartClick" />
    </div>

    <slot name="data-table"></slot>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onErrorCaptured, nextTick } from 'vue'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { 
  BarChart,
  LineChart, 
  PieChart, 
  ScatterChart, 
  HeatmapChart,
  BoxplotChart
} from 'echarts/charts'
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent,
  ToolboxComponent,
  DataZoomComponent,
  VisualMapComponent
} from 'echarts/components'
import VChart from 'vue-echarts'
import { Loading, WarningFilled, InfoFilled } from '@element-plus/icons-vue'

// 注册ECharts组件
use([
  CanvasRenderer,
  BarChart,
  LineChart,
  PieChart,
  ScatterChart,
  HeatmapChart,
  BoxplotChart,
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent,
  ToolboxComponent,
  DataZoomComponent,
  VisualMapComponent
])

const props = defineProps({
  option: {
    type: Object,
    required: true
  },
  loading: {
    type: Boolean,
    default: false
  },
  error: {
    type: Boolean,
    default: false
  },
  errorMessage: {
    type: String,
    default: '加载图表失败'
  },
  height: {
    type: String,
    default: '400px'
  },
  title: {
    type: String,
    default: ''
  },
  subtitle: {
    type: String,
    default: ''
  },
  theme: {
    type: String,
    default: 'light'
  },
  intro: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['chart-click'])

// 状态管理
const isReady = ref(false)
const internalError = ref(false)
const internalErrorMessage = ref('')

// 安全的图表配置，确保即使配置无效也不会崩溃
const safeOption = computed(() => {
  try {
    if (!props.option || typeof props.option !== 'object') return {}
    
    // 增强配置，使图表更美观
    const enhancedOption = {
      ...props.option,
      backgroundColor: props.option.backgroundColor || '#fff',
      textStyle: {
        ...props.option.textStyle,
        fontFamily: 'Arial, "Microsoft YaHei", sans-serif'
      },
      animation: true
    }
    
    // 美化图例
    if (enhancedOption.legend) {
      enhancedOption.legend = {
        ...enhancedOption.legend,
        textStyle: {
          fontSize: 12,
          color: '#333'
        },
        itemGap: 15,
        itemWidth: 15,
        itemHeight: 10,
        borderRadius: 4
      }
    }
    
    // 美化坐标轴
    if (enhancedOption.xAxis) {
      const xAxis = Array.isArray(enhancedOption.xAxis) 
        ? enhancedOption.xAxis 
        : [enhancedOption.xAxis]
        
      enhancedOption.xAxis = xAxis.map(axis => ({
        ...axis,
        axisLine: {
          lineStyle: { color: '#E0E6F1' }
        },
        axisTick: {
          lineStyle: { color: '#E0E6F1' }
        },
        axisLabel: {
          ...axis.axisLabel,
          color: '#606266',
          fontSize: 12
        },
        splitLine: {
          lineStyle: { color: '#F2F6FC' }
        }
      }))
    }
    
    if (enhancedOption.yAxis) {
      const yAxis = Array.isArray(enhancedOption.yAxis) 
        ? enhancedOption.yAxis 
        : [enhancedOption.yAxis]
        
      enhancedOption.yAxis = yAxis.map(axis => ({
        ...axis,
        axisLine: {
          lineStyle: { color: '#E0E6F1' }
        },
        axisTick: {
          lineStyle: { color: '#E0E6F1' }
        },
        axisLabel: {
          ...axis.axisLabel,
          color: '#606266',
          fontSize: 12
        },
        splitLine: {
          lineStyle: { color: '#F2F6FC' }
        }
      }))
    }
    
    // 美化提示框
    if (enhancedOption.tooltip) {
      enhancedOption.tooltip = {
        ...enhancedOption.tooltip,
        backgroundColor: 'rgba(255, 255, 255, 0.9)',
        borderColor: '#E0E6F1',
        borderWidth: 1,
        textStyle: {
          color: '#303133',
          fontSize: 12
        },
        padding: 10,
        extraCssText: 'box-shadow: 0 2px 12px 0 rgba(0,0,0,0.1)'
      }
    }
    
    return enhancedOption
  } catch (err) {
    console.error('图表配置解析错误:', err)
    return {}
  }
})

// 判断图表是否为空
const isEmpty = computed(() => {
  try {
    if (!props.option) return true
    
    // 检查是否有series或series数据为空
    const series = props.option.series
    if (!series || series.length === 0) return true
    
    // 检查series中是否有数据
    if (Array.isArray(series)) {
      return series.every(s => !s.data || s.data.length === 0)
    }
    
    return false
  } catch (err) {
    console.error('判断图表是否为空出错:', err)
    return true
  }
})

// 图表点击事件处理
const handleChartClick = (params) => {
  emit('chart-click', params)
}

// 错误处理
onErrorCaptured((err) => {
  console.log('捕获到错误:', err)
  if (String(err).includes('ResizeObserver')) {
    // 忽略ResizeObserver错误
    return false
  }
  internalError.value = true
  internalErrorMessage.value = String(err).substring(0, 100)
  return false // 阻止错误向上传播
})

// 重试加载图表
const retryChart = () => {
  isReady.value = false
  internalError.value = false
  internalErrorMessage.value = ''
  
  nextTick(() => {
    setTimeout(() => {
      isReady.value = true
    }, 300)
  })
}

// 延迟加载图表以避免ResizeObserver警告
onMounted(() => {
  try {
    // 延迟初始化图表
    setTimeout(() => {
      isReady.value = true
    }, 300)
  } catch (err) {
    console.log('图表挂载错误:', err)
  }
})
</script>

<style scoped>
.chart-container {
  position: relative;
  width: 100%;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
  padding: 20px;
  margin-bottom: 24px;
  box-sizing: border-box;
  transition: all 0.3s ease;
  overflow: visible;
  height: auto;
}

/* 添加一个选择器，针对最后一个图表容器移除底部边距 */
.chart-container:last-child {
  margin-bottom: 0;
}

.chart-container:hover {
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.12);
  transform: translateY(-2px);
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 18px;
  border-bottom: 1px solid #EBEEF5;
  padding-bottom: 12px;
  width: 100%;
}

.chart-title-area {
  flex: 1;
}

.chart-title {
  font-size: 20px;
  font-weight: bold;
  color: #303133;
  line-height: 1.4;
}

.chart-subtitle {
  font-size: 14px;
  color: #606266;
  margin-top: 6px;
  line-height: 1.4;
}

.chart-intro {
  background-color: #F0F9FF;
  border-left: 4px solid #409EFF;
  border-radius: 6px;
  padding: 14px 16px;
  margin-bottom: 20px;
  display: flex;
  align-items: flex-start;
  width: 100%;
}

.intro-icon {
  color: #409EFF;
  margin-right: 12px;
  margin-top: 2px;
  font-size: 18px;
}

.intro-text {
  color: #606266;
  font-size: 14px;
  line-height: 1.6;
  flex: 1;
}

.chart-loading, .chart-error, .chart-empty {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 320px;
  color: #909399;
  flex-direction: column;
  text-align: center;
}

.chart-loading .el-icon, .chart-error .el-icon {
  font-size: 28px;
  margin-bottom: 10px;
}

.chart-content {
  width: 100%;
  flex: 1;
  display: flex;
  flex-direction: column;
}

.chart {
  width: 100%;
  height: 100%;
  min-height: 400px;
}
</style> 