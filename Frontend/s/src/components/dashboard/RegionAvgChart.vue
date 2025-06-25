<template>
  <div class="chart-wrapper">
    <div class="chart-title">地区 × 平均赔付 条形图</div>
    <div class="chart-container" v-loading="loading" element-loading-background="rgba(15, 37, 75, 0.7)" element-loading-text="数据加载中..." element-loading-svg-view-box="-10, -10, 50, 50">
      <v-chart class="chart" :option="chartOption" autoresize />
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { use } from 'echarts/core';
import { CanvasRenderer } from 'echarts/renderers';
import { BarChart } from 'echarts/charts';
import {
  TitleComponent,
  TooltipComponent,
  GridComponent
} from 'echarts/components';
import VChart from 'vue-echarts';

use([
  CanvasRenderer,
  BarChart,
  TitleComponent,
  TooltipComponent,
  GridComponent
]);

const props = defineProps({
  data: {
    type: Object,
    default: () => ({})
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

const chartOption = computed(() => ({
  tooltip: {
    trigger: 'axis',
    axisPointer: {
      type: 'shadow'
    },
    formatter: function(params) {
      return `${params[0].name}: ${formatMoney(params[0].value)}`;
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
  grid: {
    left: '10%',
    right: '5%',
    bottom: '15%',
    top: '10%',
    containLabel: true
  },
  xAxis: {
    type: 'category',
    data: props.data ? Object.keys(props.data) : [],
    axisLine: {
      lineStyle: {
        color: '#0f6ecd'
      }
    },
    axisLabel: {
      color: '#7eb6ff',
      interval: 0,
      rotate: 45,
      fontSize: 12,
      margin: 10
    }
  },
  yAxis: {
    type: 'value',
    name: '平均医疗费用',
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
      name: '平均费用',
      type: 'bar',
      data: props.data ? Object.values(props.data) : [],
      barWidth: '40%',
      itemStyle: {
        color: function(params) {
          const colorList = [
            { 
              type: 'linear', 
              x: 0, y: 0, x2: 0, y2: 1,
              colorStops: [
                { offset: 0, color: 'rgba(0, 255, 255, 0.85)' },
                { offset: 0.5, color: 'rgba(0, 191, 255, 0.45)' },
                { offset: 1, color: 'rgba(0, 128, 255, 0.25)' }
              ]
            },
            { 
              type: 'linear', 
              x: 0, y: 0, x2: 0, y2: 1,
              colorStops: [
                { offset: 0, color: 'rgba(115, 192, 222, 0.85)' },
                { offset: 0.5, color: 'rgba(95, 158, 188, 0.45)' },
                { offset: 1, color: 'rgba(75, 124, 154, 0.25)' }
              ]
            },
            { 
              type: 'linear', 
              x: 0, y: 0, x2: 0, y2: 1,
              colorStops: [
                { offset: 0, color: 'rgba(145, 204, 117, 0.85)' },
                { offset: 0.5, color: 'rgba(118, 168, 95, 0.45)' },
                { offset: 1, color: 'rgba(91, 132, 73, 0.25)' }
              ]
            },
            { 
              type: 'linear', 
              x: 0, y: 0, x2: 0, y2: 1,
              colorStops: [
                { offset: 0, color: 'rgba(238, 196, 45, 0.85)' },
                { offset: 0.5, color: 'rgba(205, 169, 39, 0.45)' },
                { offset: 1, color: 'rgba(172, 142, 33, 0.25)' }
              ]
            },
            { 
              type: 'linear', 
              x: 0, y: 0, x2: 0, y2: 1,
              colorStops: [
                { offset: 0, color: 'rgba(250, 128, 114, 0.85)' },
                { offset: 0.5, color: 'rgba(220, 112, 100, 0.45)' },
                { offset: 1, color: 'rgba(190, 96, 86, 0.25)' }
              ]
            },
            { 
              type: 'linear', 
              x: 0, y: 0, x2: 0, y2: 1,
              colorStops: [
                { offset: 0, color: 'rgba(52, 152, 219, 0.85)' },
                { offset: 0.5, color: 'rgba(41, 120, 174, 0.45)' },
                { offset: 1, color: 'rgba(30, 88, 128, 0.25)' }
              ]
            },
            { 
              type: 'linear', 
              x: 0, y: 0, x2: 0, y2: 1,
              colorStops: [
                { offset: 0, color: 'rgba(155, 89, 182, 0.85)' },
                { offset: 0.5, color: 'rgba(125, 72, 147, 0.45)' },
                { offset: 1, color: 'rgba(95, 55, 112, 0.25)' }
              ]
            }
          ];
          return colorList[params.dataIndex % colorList.length];
        },
        borderRadius: [4, 4, 0, 0],
        shadowBlur: 10,
        shadowColor: 'rgba(0, 255, 255, 0.3)'
      },
      label: {
        show: true,
        position: 'top',
        formatter: function(params) {
          return formatMoney(params.value);
        },
        color: '#fff',
        fontSize: 11,
        distance: 5
      }
    }
  ]
}));
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