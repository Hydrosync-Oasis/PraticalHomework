<template>
  <div class="chart-wrapper">
    <div class="chart-title">相关系数热力图</div>
    <div class="chart-container" v-loading="loading" element-loading-background="rgba(15, 37, 75, 0.7)" element-loading-text="数据加载中..." element-loading-svg-view-box="-10, -10, 50, 50">
      <v-chart class="chart" :option="chartOption" autoresize />
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { use } from 'echarts/core';
import { CanvasRenderer } from 'echarts/renderers';
import { HeatmapChart } from 'echarts/charts';
import {
  TitleComponent,
  TooltipComponent,
  GridComponent,
  VisualMapComponent
} from 'echarts/components';
import VChart from 'vue-echarts';

use([
  CanvasRenderer,
  HeatmapChart,
  TitleComponent,
  TooltipComponent,
  GridComponent,
  VisualMapComponent
]);

const props = defineProps({
  data: {
    type: Array,
    default: () => []
  },
  loading: {
    type: Boolean,
    default: false
  }
});

// 计算相关性矩阵
function calculateCorrelation(data) {
  if (!data || data.length === 0) return [];
  
  const result = [];
  const features = ['年龄', 'BMI', '子女数', '医疗费用'];
  
  // 提取每个特征的数据
  const age = data.map(item => item[0]);
  const bmi = data.map(item => item[1]);
  const children = data.map(item => item[2]);
  const charges = data.map(item => item[3]);
  
  const allFeatures = [age, bmi, children, charges];
  
  // 计算相关性矩阵
  for (let i = 0; i < features.length; i++) {
    for (let j = 0; j < features.length; j++) {
      const corr = i === j ? 1 : pearsonCorrelation(allFeatures[i], allFeatures[j]);
      result.push([i, j, corr]);
    }
  }
  
  return result;
}

// 计算皮尔逊相关系数
function pearsonCorrelation(x, y) {
  const n = x.length;
  let sumX = 0, sumY = 0, sumXY = 0, sumX2 = 0, sumY2 = 0;
  
  for (let i = 0; i < n; i++) {
    sumX += x[i];
    sumY += y[i];
    sumXY += x[i] * y[i];
    sumX2 += x[i] * x[i];
    sumY2 += y[i] * y[i];
  }
  
  const numerator = n * sumXY - sumX * sumY;
  const denominator = Math.sqrt((n * sumX2 - sumX * sumX) * (n * sumY2 - sumY * sumY));
  
  return denominator === 0 ? 0 : numerator / denominator;
}

// 格式化相关系数，保留两位小数
function formatCorrelation(value) {
  return value.toFixed(2);
}

const chartOption = computed(() => {
  const correlationData = calculateCorrelation(props.data);
  
  return {
    tooltip: {
      position: 'top',
      formatter: function(params) {
        const features = ['年龄', 'BMI', '子女数', '医疗费用'];
        const x = features[params.value[0]];
        const y = features[params.value[1]];
        const value = formatCorrelation(params.value[2]);
        return `${x} 与 ${y} 的相关系数: ${value}`;
      },
      backgroundColor: 'rgba(15, 37, 75, 0.85)',
      borderColor: 'rgba(15, 110, 205, 0.5)',
      borderWidth: 1,
      padding: [8, 12],
      textStyle: {
        color: '#fff',
        fontSize: 12
      }
    },
    animation: true,
    grid: {
      height: '65%',
      left: '18%',
      right: '10%',
      top: '15%',
      bottom: '22%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: ['年龄', 'BMI', '子女数', '医疗费用'],
      axisLine: {
        lineStyle: {
          color: '#0f6ecd'
        }
      },
      axisLabel: {
        color: '#7eb6ff',
        interval: 0,
        fontSize: 12,
        margin: 8,
        rotate: 0
      },
      splitArea: {
        show: true,
        areaStyle: {
          color: ['rgba(15, 37, 75, 0.02)', 'rgba(15, 37, 75, 0.05)']
        }
      }
    },
    yAxis: {
      type: 'category',
      data: ['年龄', 'BMI', '子女数', '医疗费用'],
      axisLine: {
        lineStyle: {
          color: '#0f6ecd'
        }
      },
      axisLabel: {
        color: '#7eb6ff',
        interval: 0,
        fontSize: 12,
        margin: 8
      },
      splitArea: {
        show: true,
        areaStyle: {
          color: ['rgba(15, 37, 75, 0.02)', 'rgba(15, 37, 75, 0.05)']
        }
      }
    },
    visualMap: {
      min: -1,
      max: 1,
      calculable: true,
      orient: 'vertical',
      left: '2%',
      bottom: '15%',
      top: '15%',
      precision: 2,
      itemWidth: 15,
      itemHeight: 80,
      inRange: {
        color: ['#313695', '#4575b4', '#74add1', '#abd9e9', '#e0f3f8', 
                '#ffffbf', '#fee090', '#fdae61', '#f46d43', '#d73027', '#a50026']
      },
      textStyle: {
        color: '#fff',
        fontSize: 10
      },
      itemGap: 10,
      formatter: function (value) {
        return value.toFixed(2);
      },
      textGap: 10,
      align: 'center',
      padding: [0, 0, 0, 0]
    },
    series: [
      {
        name: '相关性系数',
        type: 'heatmap',
        data: correlationData,
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowColor: 'rgba(0, 255, 255, 0.5)'
          }
        },
        label: {
          show: true,
          formatter: function(params) {
            return formatCorrelation(params.value[2]);
          },
          fontSize: 11,
          fontWeight: 'bold',
          color: function(params) {
            const value = params.value[2];
            return Math.abs(value) > 0.5 ? '#fff' : '#333';
          }
        },
        itemStyle: {
          borderWidth: 1,
          borderColor: 'rgba(15, 110, 205, 0.3)'
        }
      }
    ]
  };
});
</script>

<style scoped>
.chart-wrapper {
  height: 100%;
  width: 100%;
  display: flex;
  flex-direction: column;
  margin-top: -10px;
  margin-bottom: -10px;
}

.chart-title {
  height: 40px;
  line-height: 40px;
  padding: 0 15px;
  font-size: 14px;
  color: #00FFFF;
  border-bottom: 1px solid rgba(15, 110, 205, 0.5);
  background-color: rgba(15, 37, 75, 0.8);
  font-weight: bold;
  text-align: center;
}

.chart-container {
  flex: 1;
  width: 100%;
}

.chart {
  width: 100%;
  height: 100%;
}
</style> 