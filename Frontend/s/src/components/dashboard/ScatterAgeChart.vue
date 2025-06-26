<template>
  <div class="chart-wrapper">
    <div class="chart-title">年龄 vs 医保费用 (按吸烟状态)</div>
    <div class="chart-container" v-loading="loading" element-loading-background="rgba(15, 37, 75, 0.7)" element-loading-text="数据加载中..." element-loading-svg-view-box="-10, -10, 50, 50">
      <v-chart class="chart" :option="chartOption" autoresize />
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { use } from 'echarts/core';
import { CanvasRenderer } from 'echarts/renderers';
import { ScatterChart } from 'echarts/charts';
import {
  TitleComponent,
  TooltipComponent,
  GridComponent,
  LegendComponent
} from 'echarts/components';
import VChart from 'vue-echarts';

use([
  CanvasRenderer,
  ScatterChart,
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

// 格式化金额，统一显示格式
function formatMoney(value) {
  return `$${Math.round(value).toLocaleString()}`;
}

const chartOption = computed(() => {
  // 确保 data 不为 null 或 undefined
  const safeData = props.data || [];
  
  // 将数据分为吸烟者和非吸烟者两组
  const smokerData = safeData.filter(item => item[2] === 'yes').map(item => [item[0], item[1]]);
  const nonSmokerData = safeData.filter(item => item[2] === 'no').map(item => [item[0], item[1]]);
  
  // 计算平均值
  const smokerAvg = smokerData.length > 0 
    ? smokerData.reduce((sum, item) => sum + item[1], 0) / smokerData.length 
    : 0;
    
  const nonSmokerAvg = nonSmokerData.length > 0 
    ? nonSmokerData.reduce((sum, item) => sum + item[1], 0) / nonSmokerData.length 
    : 0;
  
  return {
    tooltip: {
      trigger: 'item',
      formatter: function(params) {
        if (params.seriesIndex <= 1) {
          const smokerStatus = params.seriesIndex === 0 ? '吸烟者' : '非吸烟者';
          return `${smokerStatus}<br/>年龄: ${params.value[0]}岁<br/>医保费用: ${formatMoney(params.value[1])}`;
        } else {
          return `${params.seriesName}: ${formatMoney(params.value)}`;
        }
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
      data: ['吸烟者', '非吸烟者', '吸烟者平均', '非吸烟者平均'],
      textStyle: {
        color: '#fff',
        fontSize: 12
      },
      bottom: 0,
      padding: [5, 10]
    },
    grid: {
      left: '10%',
      right: '5%',
      bottom: '15%',
      top: '15%',
      containLabel: true
    },
    xAxis: {
      type: 'value',
      name: '',
      nameLocation: 'middle',
      nameGap: 30,
      nameTextStyle: {
        color: '#7eb6ff',
        fontSize: 12,
        padding: [10, 0, 0, 0]
      },
      min: function(value) {
        return Math.floor(value.min - 2);
      },
      max: function(value) {
        return Math.ceil(value.max + 2);
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
        fontSize: 12,
        formatter: '{value}岁'
      }
    },
    yAxis: {
      type: 'value',
      name: '医保费用',
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
        fontSize: 12,
        formatter: function(value) {
          if (value >= 1000) {
            return `$${value/1000}k`;
          }
          return `$${value}`;
        }
      }
    },
    series: [
      {
        name: '吸烟者',
        type: 'scatter',
        data: smokerData,
        symbolSize: 10,
        itemStyle: {
          color: '#FF6384',
          opacity: 0.7,
          borderColor: '#fff',
          borderWidth: 1
        },
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowColor: 'rgba(255, 99, 132, 0.5)'
          }
        }
      },
      {
        name: '非吸烟者',
        type: 'scatter',
        data: nonSmokerData,
        symbolSize: 10,
        itemStyle: {
          color: '#36A2EB',
          opacity: 0.7,
          borderColor: '#fff',
          borderWidth: 1
        },
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowColor: 'rgba(54, 162, 235, 0.5)'
          }
        }
      },
      {
        name: '吸烟者平均',
        type: 'line',
        markLine: {
          silent: true,
          symbol: 'none',
          lineStyle: {
            color: '#FF6384',
            type: 'dashed',
            width: 2
          },
          data: [
            {
              yAxis: smokerAvg,
              label: {
                formatter: `吸烟者平均: ${formatMoney(smokerAvg)}`,
                position: 'end',
                color: '#fff',
                backgroundColor: 'rgba(255, 99, 132, 0.7)',
                borderRadius: 3,
                padding: [3, 5],
                fontSize: 12
              }
            }
          ]
        },
        data: []
      },
      {
        name: '非吸烟者平均',
        type: 'line',
        markLine: {
          silent: true,
          symbol: 'none',
          lineStyle: {
            color: '#36A2EB',
            type: 'dashed',
            width: 2
          },
          data: [
            {
              yAxis: nonSmokerAvg,
              label: {
                formatter: `非吸烟者平均: ${formatMoney(nonSmokerAvg)}`,
                position: 'end',
                color: '#fff',
                backgroundColor: 'rgba(54, 162, 235, 0.7)',
                borderRadius: 3,
                padding: [3, 5],
                fontSize: 12
              }
            }
          ]
        },
        data: []
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
  display: flex;
  align-items: center;
  justify-content: center;
  padding-top: 4px;
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