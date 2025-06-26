<template>
  <div class="chart-wrapper">
    <div class="chart-title">BMI vs 医保赔付 散点图</div>
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
  GridComponent
} from 'echarts/components';
import VChart from 'vue-echarts';

use([
  CanvasRenderer,
  ScatterChart,
  TitleComponent,
  TooltipComponent,
  GridComponent
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

// 计算BMI与医保费用的趋势线
function calculateTrendLine(data) {
  if (!data || data.length < 2) return [[0, 0], [0, 0]];
  
  // 提取 x 和 y 值
  const xValues = data.map(item => item[0]);
  const yValues = data.map(item => item[1]);
  
  // 计算线性回归
  const n = xValues.length;
  let sumX = 0, sumY = 0, sumXY = 0, sumX2 = 0;
  
  for (let i = 0; i < n; i++) {
    sumX += xValues[i];
    sumY += yValues[i];
    sumXY += xValues[i] * yValues[i];
    sumX2 += xValues[i] * xValues[i];
  }
  
  const slope = (n * sumXY - sumX * sumY) / (n * sumX2 - sumX * sumX);
  const intercept = (sumY - slope * sumX) / n;
  
  // 获取最小和最大 x 值
  const minX = Math.min(...xValues);
  const maxX = Math.max(...xValues);
  
  // 创建趋势线的两个点
  return [
    [minX, slope * minX + intercept],
    [maxX, slope * maxX + intercept]
  ];
}

const chartOption = computed(() => {
  // 确保 data 不为 null 或 undefined
  const safeData = props.data || [];
  
  // 计算趋势线
  const trendLineData = calculateTrendLine(safeData);
  
  // 计算相关系数
  let correlation = 0;
  if (safeData && safeData.length > 2) {
    const xValues = safeData.map(item => item[0]);
    const yValues = safeData.map(item => item[1]);
    
    const n = xValues.length;
    let sumX = 0, sumY = 0, sumXY = 0, sumX2 = 0, sumY2 = 0;
    
    for (let i = 0; i < n; i++) {
      sumX += xValues[i];
      sumY += yValues[i];
      sumXY += xValues[i] * yValues[i];
      sumX2 += xValues[i] * xValues[i];
      sumY2 += yValues[i] * yValues[i];
    }
    
    const numerator = n * sumXY - sumX * sumY;
    const denominator = Math.sqrt((n * sumX2 - sumX * sumX) * (n * sumY2 - sumY * sumY));
    
    correlation = denominator === 0 ? 0 : (numerator / denominator).toFixed(2);
  }
  
  return {
    tooltip: {
      trigger: 'item',
      formatter: function(params) {
        if (params.seriesIndex === 0) {
          return `BMI: ${params.value[0].toFixed(1)}<br/>医保费用: ${formatMoney(params.value[1])}`;
        } else {
          return '趋势线';
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
      data: ['BMI与医保费用', '趋势线'],
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
      name: 'BMI指数',
      nameLocation: 'middle',
      nameGap: 30,
      nameTextStyle: {
        color: '#7eb6ff',
        fontSize: 12,
        padding: [10, 0, 0, 0]
      },
      min: function(value) {
        return Math.floor(value.min - 1);
      },
      max: function(value) {
        return Math.ceil(value.max + 1);
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
        formatter: '{value}'
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
        name: 'BMI与医保费用',
        type: 'scatter',
        data: safeData,
        symbolSize: function(data) {
          // 根据医保费用调整点的大小
          return Math.sqrt(data[1]) / 50 + 5;
        },
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowColor: 'rgba(0, 255, 255, 0.5)'
          }
        },
        itemStyle: {
          color: function(params) {
            // 根据BMI值设置颜色
            const bmi = params.data[0];
            if (bmi < 18.5) {
              return '#91CC75'; // 偏瘦
            } else if (bmi < 25) {
              return '#73C0DE'; // 正常
            } else if (bmi < 30) {
              return '#FFCE56'; // 超重
            } else {
              return '#FF6384'; // 肥胖
            }
          },
          opacity: 0.7,
          borderColor: '#fff',
          borderWidth: 1
        }
      },
      {
        name: '趋势线',
        type: 'line',
        data: trendLineData,
        showSymbol: false,
        smooth: false,
        lineStyle: {
          color: '#00FFFF',
          width: 1.5,
          type: 'dashed'
        },
        markPoint: {
          symbolSize: 0,
          label: {
            show: true,
            formatter: `相关系数: ${correlation}`,
            color: '#fff',
            backgroundColor: 'rgba(15, 37, 75, 0.7)',
            borderRadius: 3,
            padding: [3, 5],
            position: 'right'
          },
          data: [
            {
              coord: trendLineData[0],
              symbolOffset: [0, 30]
            }
          ]
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
}

.chart {
  width: 100%;
  height: 100%;
}
</style> 