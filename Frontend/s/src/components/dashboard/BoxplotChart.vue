<template>
  <div class="chart-wrapper">
    <div class="chart-title">吸烟状态 vs 医保赔付箱线图</div>
    <div class="chart-container" v-loading="loading" element-loading-background="rgba(15, 37, 75, 0.7)" element-loading-text="数据加载中..." element-loading-svg-view-box="-10, -10, 50, 50">
      <v-chart class="chart" :option="chartOption" autoresize />
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { use } from 'echarts/core';
import { CanvasRenderer } from 'echarts/renderers';
import { BoxplotChart } from 'echarts/charts';
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent
} from 'echarts/components';
import VChart from 'vue-echarts';

use([
  CanvasRenderer,
  BoxplotChart,
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent
]);

const props = defineProps({
  data: {
    type: Object,
    default: () => ({ yes: [], no: [] })
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

// 计算箱线图数据
function calculateBoxplotData(data) {
  if (!data || data.length === 0) return [0, 0, 0, 0, 0];
  
  // 数据排序
  const sortedData = [...data].sort((a, b) => a - b);
  
  const len = sortedData.length;
  const q1 = sortedData[Math.floor(len * 0.25)];
  const median = sortedData[Math.floor(len * 0.5)];
  const q3 = sortedData[Math.floor(len * 0.75)];
  const min = sortedData[0];
  const max = sortedData[len - 1];
  
  return [min, q1, median, q3, max];
}

const chartOption = computed(() => {
  // 确保 data 不为 null，如果为 null 则使用默认空数组
  const safeData = props.data || { yes: [], no: [] };
  
  // 计算吸烟者和非吸烟者的平均医保费用
  const smokerAvg = safeData.yes.length > 0 
    ? safeData.yes.reduce((sum, val) => sum + val, 0) / safeData.yes.length 
    : 0;
    
  const nonSmokerAvg = safeData.no.length > 0 
    ? safeData.no.reduce((sum, val) => sum + val, 0) / safeData.no.length 
    : 0;
  
  return {
    tooltip: {
      trigger: 'item',
      formatter: function(params) {
        if (params.seriesIndex === 0) {
          if (params.dataIndex === 0) {
            return `非吸烟者医保费用:<br/>
                    最小值: ${formatMoney(params.data[1])}<br/>
                    下四分位: ${formatMoney(params.data[2])}<br/>
                    中位数: ${formatMoney(params.data[3])}<br/>
                    上四分位: ${formatMoney(params.data[4])}<br/>
                    最大值: ${formatMoney(params.data[5])}`;
          } else {
            return `吸烟者医保费用:<br/>
                    最小值: ${formatMoney(params.data[1])}<br/>
                    下四分位: ${formatMoney(params.data[2])}<br/>
                    中位数: ${formatMoney(params.data[3])}<br/>
                    上四分位: ${formatMoney(params.data[4])}<br/>
                    最大值: ${formatMoney(params.data[5])}`;
          }
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
      data: ['箱线图', '平均值'],
      textStyle: {
        color: '#fff',
        fontSize: 12
      },
      bottom: 0,
      padding: [5, 10],
      selectedMode: false
    },
    grid: {
      left: '10%',
      right: '10%',
      bottom: '15%',
      top: '15%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: ['非吸烟者', '吸烟者'],
      axisLine: {
        lineStyle: {
          color: '#0f6ecd'
        }
      },
      axisLabel: {
        color: '#7eb6ff',
        fontSize: 12,
        margin: 10
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
        name: '箱线图',
        type: 'boxplot',
        data: [
          calculateBoxplotData(safeData.no),
          calculateBoxplotData(safeData.yes)
        ],
        itemStyle: {
          color: function(params) {
            return params.dataIndex === 0 ? 'rgba(115, 192, 222, 0.5)' : 'rgba(238, 102, 102, 0.5)';
          },
          borderColor: function(params) {
            return params.dataIndex === 0 ? '#5470C6' : '#FF6384';
          },
          borderWidth: 2,
          shadowBlur: 5,
          shadowColor: 'rgba(0, 0, 0, 0.2)'
        },
        tooltip: {
          formatter: function(params) {
            return `${params.name}:<br/>
                   最小值: ${formatMoney(params.data[1])}<br/>
                   下四分位: ${formatMoney(params.data[2])}<br/>
                   中位数: ${formatMoney(params.data[3])}<br/>
                   上四分位: ${formatMoney(params.data[4])}<br/>
                   最大值: ${formatMoney(params.data[5])}`;
          }
        }
      },
      {
        name: '平均值',
        type: 'scatter',
        data: [
          {
            value: nonSmokerAvg,
            itemStyle: { color: '#5470C6' }
          },
          {
            value: smokerAvg,
            itemStyle: { color: '#FF6384' }
          }
        ],
        symbolSize: 10,
        symbol: 'diamond',
        label: {
          show: true,
          position: 'top',
          formatter: function(params) {
            return `平均: ${formatMoney(params.value)}`;
          },
          color: '#fff',
          fontSize: 12,
          backgroundColor: 'rgba(15, 37, 75, 0.7)',
          borderRadius: 3,
          padding: [3, 5],
          distance: 10,
          offset: [0, 5]
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