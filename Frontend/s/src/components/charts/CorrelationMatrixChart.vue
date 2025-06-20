<template>
  <div class="correlation-matrix-charts">
    <chart-wrapper 
      title="特征相关性热力图" 
      subtitle="不同特征之间的相关程度"
      intro="本热力图展示了各个特征之间的相关性强度，颜色越深表示相关性越强，红色代表正相关，蓝色代表负相关。通过分析特征之间的相关性，可以识别与肺癌诊断最相关的关键因素。"
      :option="heatmapOption" 
      :loading="loading"
      :error="error"
      :error-message="errorMessage"
      height="600px"/>
      
    <div class="high-correlation-container">
      <h3 class="section-title">高相关性特征对</h3>
      <el-table
        :data="highCorrelationData"
        style="width: 100%"
        :cell-style="cellStyle"
        max-height="400px"
        v-if="!loading && !error && highCorrelationData.length > 0">
        <el-table-column prop="feature1" label="特征1" width="180" />
        <el-table-column prop="feature2" label="特征2" width="180" />
        <el-table-column prop="correlation" label="相关性系数">
          <template #default="scope">
            <div class="correlation-value">
              {{ scope.row.correlation }}
              <span class="correlation-bar" 
                :style="{ 
                  width: Math.abs(scope.row.correlation) * 100 + '%',
                  backgroundColor: scope.row.correlation > 0 ? '#e74c3c' : '#3498db'
                }"></span>
            </div>
          </template>
        </el-table-column>
      </el-table>
      <el-empty description="暂无数据" v-else-if="!loading && !error"></el-empty>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import ChartWrapper from '../ChartWrapper.vue'
import { analysisApi } from '@/services/api'

// 状态
const chartData = ref(null)
const loading = ref(false)
const error = ref(false)
const errorMessage = ref('')

// 热力图配置
const heatmapOption = computed(() => {
  if (!chartData.value) return {}
  
  const { categories, data } = chartData.value.correlationMatrix
  
  return {
    tooltip: {
      position: 'top',
      formatter: function (params) {
        return `${categories[params.data[1]]} 与 ${categories[params.data[0]]} 的相关性: ${params.data[2]}`
      }
    },
    grid: {
      left: '15%',
      right: '10%',
      top: '10%',
      bottom: '20%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: categories,
      splitArea: {
        show: true
      },
      axisLabel: {
        interval: 0,
        rotate: 45,
        fontSize: 12,
        margin: 8,
        formatter: function(value) {
          // 限制标签长度
          if(value.length > 10) {
            return value.substring(0, 10) + '...'
          }
          return value
        }
      }
    },
    yAxis: {
      type: 'category',
      data: categories,
      splitArea: {
        show: true
      },
      axisLabel: {
        interval: 0,
        fontSize: 12,
        formatter: function(value) {
          // 限制标签长度
          if(value.length > 10) {
            return value.substring(0, 10) + '...'
          }
          return value
        }
      }
    },
    visualMap: {
      min: -1,
      max: 1,
      calculable: true,
      orient: 'horizontal',
      left: 'center',
      bottom: 0,
      inRange: {
        color: ['#313695', '#4575b4', '#74add1', '#abd9e9', '#e0f3f8', '#ffffbf', '#fee090', '#fdae61', '#f46d43', '#d73027', '#a50026']
      }
    },
    dataZoom: [
      {
        type: 'slider',
        show: true,
        xAxisIndex: [0],
        start: 0,
        end: 100
      },
      {
        type: 'slider',
        show: true,
        yAxisIndex: [0],
        start: 0,
        end: 100
      },
      {
        type: 'inside',
        xAxisIndex: 0,
        start: 0,
        end: 100
      },
      {
        type: 'inside',
        yAxisIndex: 0,
        start: 0,
        end: 100
      }
    ],
    toolbox: {
      feature: {
        dataZoom: {
          yAxisIndex: 'none'
        },
        restore: {},
        saveAsImage: {}
      },
      right: 10,
      top: 0
    },
    series: [
      {
        name: '相关性',
        type: 'heatmap',
        data: data,
        label: {
          show: true,
          fontSize: 10
        },
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowColor: 'rgba(0, 0, 0, 0.5)'
          }
        }
      }
    ]
  }
})

// 高相关性特征数据
const highCorrelationData = computed(() => {
  if (!chartData.value || !chartData.value.highCorrelation) return []
  return chartData.value.highCorrelation
})

// 表格单元格样式
const cellStyle = ({ row, column }) => {
  if (column.property === 'correlation') {
    return {
      color: row.correlation > 0 ? '#e74c3c' : '#3498db',
      fontWeight: Math.abs(row.correlation) > 0.7 ? 'bold' : 'normal'
    }
  }
}

// 获取数据
const fetchData = async () => {
  loading.value = true
  error.value = false
  
  try {
    const response = await analysisApi.getCorrelationMatrix()
    chartData.value = response.data
  } catch (err) {
    console.error('获取相关性矩阵数据失败:', err)
    error.value = true
    errorMessage.value = '获取数据失败: ' + (err.message || '未知错误')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchData()
})
</script>

<style scoped>
.correlation-matrix-charts {
  display: flex;
  flex-direction: column;
  gap: 20px;
  width: 100%;
  overflow: visible;
}

.high-correlation-container {
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  padding: 16px;
  width: 100%;
  overflow: auto;
}

.section-title {
  margin-top: 0;
  margin-bottom: 16px;
  font-size: 18px;
  font-weight: bold;
}

.correlation-value {
  position: relative;
  width: 100%;
  text-align: left;
  padding-right: 50px;
}

.correlation-bar {
  position: absolute;
  top: 50%;
  right: 0;
  height: 8px;
  transform: translateY(-50%);
  border-radius: 4px;
}

:deep(.el-table__body-wrapper) {
  overflow-y: auto;
}

:deep(.el-table) {
  width: 100% !important;
}
</style> 