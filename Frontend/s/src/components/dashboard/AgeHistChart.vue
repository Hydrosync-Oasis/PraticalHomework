<template>
  <div class="chart-wrapper">
    <div class="chart-title">年龄直方图</div>
    <div class="stats-row">
      <div class="stat-box">
        <div class="stat-num">{{ avgAge.toFixed(1) }}</div>
        <div class="stat-label">平均年龄</div>
      </div>
      <div class="stat-box">
        <div class="stat-num">{{ minAge }}</div>
        <div class="stat-label">最小年龄</div>
      </div>
      <div class="stat-box">
        <div class="stat-num">{{ maxAge }}</div>
        <div class="stat-label">最大年龄</div>
      </div>
    </div>
    <div class="chart-container" v-loading="loading" element-loading-background="rgba(15, 37, 75, 0.7)" element-loading-text="数据加载中..." element-loading-svg-view-box="-10, -10, 50, 50">
      <v-chart class="chart" :option="chartOption" autoresize />
    </div>
  </div>
</template>

<script setup>
import { computed, ref, watch } from 'vue';
import { use } from 'echarts/core';
import { CanvasRenderer } from 'echarts/renderers';
import { BarChart, LineChart } from 'echarts/charts';
import {
  TitleComponent,
  TooltipComponent,
  GridComponent,
  LegendComponent
} from 'echarts/components';
import VChart from 'vue-echarts';

use([
  CanvasRenderer,
  BarChart,
  LineChart,
  TitleComponent,
  TooltipComponent,
  GridComponent,
  LegendComponent
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

// 年龄统计数据
const avgAge = ref(0);
const minAge = ref(0);
const maxAge = ref(0);

// 格式化数字，统一保留1位小数
function formatNumber(value, type = 'decimal') {
  if (value === undefined || value === null) return '0';
  
  switch (type) {
    case 'percent':
      return `${value.toFixed(1)}%`;
    case 'decimal':
      return value.toFixed(1);
    default:
      return value.toString();
  }
}

// 处理年龄直方图数据
function processAgeHistData(data) {
  if (!data || data.length === 0) {
    return {
      ageGroups: [0, 0, 0, 0, 0],
      ageLabels: ['18-25', '26-35', '36-45', '46-55', '56-65']
    };
  }
  
  // 计算基本统计数据
  minAge.value = Math.min(...data);
  maxAge.value = Math.max(...data);
  avgAge.value = data.reduce((a, b) => a + b, 0) / data.length;
  
  // 定义年龄组
  const ageGroups = [0, 0, 0, 0, 0];
  const ageLabels = ['18-25', '26-35', '36-45', '46-55', '56-65'];
  
  // 统计各年龄组人数
  data.forEach(age => {
    if (age < 26) {
      ageGroups[0]++;
    } else if (age < 36) {
      ageGroups[1]++;
    } else if (age < 46) {
      ageGroups[2]++;
    } else if (age < 56) {
      ageGroups[3]++;
    } else {
      ageGroups[4]++;
    }
  });
  
  return { ageGroups, ageLabels };
}

// 监听数据变化，更新统计值
watch(() => props.data, (newData) => {
  if (newData && newData.length > 0) {
    minAge.value = Math.min(...newData);
    maxAge.value = Math.max(...newData);
    avgAge.value = newData.reduce((a, b) => a + b, 0) / newData.length;
  } else {
    minAge.value = 0;
    maxAge.value = 0;
    avgAge.value = 0;
  }
}, { immediate: true });

const chartOption = computed(() => {
  const processedData = processAgeHistData(props.data);
  
  return {
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      },
      formatter: function(params) {
        const barData = params[0];
        const lineData = params[1];
        const total = processedData.ageGroups.reduce((a, b) => a + b, 0);
        const percentage = total > 0 ? (barData.value / total * 100).toFixed(1) : 0;
        
        return `${barData.name}岁:<br/>
                人数: ${barData.value}人<br/>
                占比: ${percentage}%<br/>
                趋势: ${lineData.value}%`;
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
    legend: {
      data: ['患者数量', '年龄分布趋势'],
      textStyle: {
        color: '#fff',
        fontSize: 12
      },
      bottom: 0,
      padding: [5, 10]
    },
    grid: {
      left: '10%',
      right: '10%',
      bottom: '15%',
      top: '25%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      name: '年龄段',
      nameLocation: 'middle',
      nameGap: 30,
      nameTextStyle: {
        color: '#7eb6ff',
        fontSize: 12,
        padding: [10, 0, 0, 0]
      },
      data: processedData.ageLabels,
      axisLine: {
        lineStyle: {
          color: '#0f6ecd'
        }
      },
      axisLabel: {
        color: '#7eb6ff',
        fontSize: 12,
        interval: 0
      }
    },
    yAxis: [
      {
        type: 'value',
        name: '人数',
        nameLocation: 'middle',
        nameGap: 40,
        nameTextStyle: {
          color: '#7eb6ff',
          fontSize: 12,
          padding: [0, 0, 5, 0]
        },
        splitLine: {
          lineStyle: {
            color: 'rgba(15, 110, 205, 0.3)'
          }
        },
        axisLine: {
          lineStyle: {
            color: '#0f6ecd'
          }
        },
        axisLabel: {
          color: '#7eb6ff',
          fontSize: 12
        }
      },
      {
        type: 'value',
        name: '',
        nameLocation: 'middle',
        nameGap: 40,
        min: 0,
        max: 100,
        nameTextStyle: {
          color: '#7eb6ff',
          fontSize: 12,
          padding: [0, 0, 5, 0]
        },
        splitLine: {
          show: false
        },
        axisLine: {
          lineStyle: {
            color: '#0f6ecd'
          }
        },
        axisLabel: {
          color: '#7eb6ff',
          fontSize: 12,
          formatter: '{value}%'
        }
      }
    ],
    series: [
      {
        name: '患者数量',
        type: 'bar',
        barWidth: '40%',
        data: processedData.ageGroups,
        itemStyle: {
          color: {
            type: 'linear',
            x: 0,
            y: 0,
            x2: 0,
            y2: 1,
            colorStops: [
              { offset: 0, color: 'rgba(0, 255, 255, 0.85)' },
              { offset: 0.5, color: 'rgba(0, 191, 255, 0.45)' },
              { offset: 1, color: 'rgba(0, 128, 255, 0.25)' }
            ]
          },
          borderRadius: [4, 4, 0, 0],
          shadowBlur: 10,
          shadowColor: 'rgba(0, 255, 255, 0.3)'
        },
        emphasis: {
          itemStyle: {
            color: {
              type: 'linear',
              x: 0,
              y: 0,
              x2: 0,
              y2: 1,
              colorStops: [
                { offset: 0, color: 'rgba(0, 255, 255, 0.95)' },
                { offset: 0.5, color: 'rgba(0, 191, 255, 0.65)' },
                { offset: 1, color: 'rgba(0, 128, 255, 0.45)' }
              ]
            }
          }
        },
        label: {
          show: true,
          position: 'top',
          color: '#fff',
          fontSize: 12
        }
      },
      {
        name: '年龄分布趋势',
        type: 'line',
        yAxisIndex: 1,
        smooth: true,
        symbol: 'circle',
        symbolSize: 8,
        data: processedData.ageGroups.map(val => {
          const total = processedData.ageGroups.reduce((a, b) => a + b, 0);
          return total > 0 ? parseFloat((val / total * 100).toFixed(1)) : 0;
        }),
        lineStyle: {
          color: '#FF77FF',
          width: 3
        },
        itemStyle: {
          color: '#FF77FF',
          borderColor: '#fff',
          borderWidth: 1
        },
        label: {
          show: false
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
  position: relative;
}

.chart {
  width: 100%;
  height: 100%;
}

.stats-row {
  display: flex;
  justify-content: space-around;
  padding: 5px 0;
  background-color: rgba(15, 37, 75, 0.6);
  border-bottom: 1px solid rgba(15, 110, 205, 0.5);
}

.stat-box {
  text-align: center;
  padding: 5px 10px;
  background-color: rgba(15, 37, 75, 0.8);
  border-radius: 4px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
}

.stat-num {
  font-size: 16px;
  font-weight: bold;
  color: #00FFFF;
}

.stat-label {
  font-size: 12px;
  color: #7eb6ff;
  margin-top: 2px;
}
</style> 