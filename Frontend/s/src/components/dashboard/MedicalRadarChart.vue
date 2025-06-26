<template>
  <div class="chart-wrapper">
    <div class="chart-title">医保数据综合分析雷达图</div>
    <div class="chart-container" v-loading="loading" element-loading-background="rgba(15, 37, 75, 0.7)" element-loading-text="数据加载中..." element-loading-svg-view-box="-10, -10, 50, 50">
      <v-chart class="chart" :option="chartOption" autoresize />
    </div>
    <div class="chart-indicators">
      <div class="indicator-item" v-for="(item, index) in indicatorExplanations" :key="index">
        <div class="indicator-color" :style="{backgroundColor: indicatorColors[index]}"></div>
        <div class="indicator-text">
          <div class="indicator-name">{{ item.name }}</div>
          <div class="indicator-value">{{ item.value }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue';
import { use } from 'echarts/core';
import { CanvasRenderer } from 'echarts/renderers';
import { RadarChart } from 'echarts/charts';
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent
} from 'echarts/components';
import VChart from 'vue-echarts';

use([
  CanvasRenderer,
  RadarChart,
  TitleComponent,
  TooltipComponent,
  LegendComponent
]);

const props = defineProps({
  boxplotData: {
    type: Object,
    default: () => ({ yes: [], no: [] })
  },
  scatterBmiData: {
    type: Array,
    default: () => []
  },
  ageHistData: {
    type: Array,
    default: () => []
  },
  regionAvgData: {
    type: Object,
    default: () => ({})
  },
  scatterAgeData: {
    type: Array,
    default: () => []
  },
  correlationData: {
    type: Array,
    default: () => []
  },
  loading: {
    type: Boolean,
    default: false
  }
});

// 指标颜色
const indicatorColors = [
  '#FF6384', // 吸烟者医保费用
  '#36A2EB', // 非吸烟者医保费用
  '#FFCE56', // 平均BMI指数
  '#4BC0C0', // 平均年龄
  '#9966FF', // 地区医保费用差异
  '#FF9F40', // 年龄-医保费用相关性
  '#C9CBCF'  // BMI-医保费用相关性
];

// 计算综合数据指标
const indicatorExplanations = ref([]);

// 格式化数字，统一保留1位小数
function formatNumber(value, type = 'default') {
  if (value === undefined || value === null) return '0';
  
  switch (type) {
    case 'money':
      return `$${Math.round(value).toLocaleString()}`;
    case 'percent':
      return `${value.toFixed(1)}%`;
    case 'decimal':
      return value.toFixed(1);
    case 'correlation':
      return value.toFixed(2);
    default:
      return value.toString();
  }
}

const chartOption = computed(() => {
  // 1. 计算吸烟者与非吸烟者的平均医保费用
  const smokerCharges = props.boxplotData?.yes?.length 
    ? props.boxplotData.yes.reduce((acc, val) => acc + val, 0) / props.boxplotData.yes.length
    : 0;
  
  const nonSmokerCharges = props.boxplotData?.no?.length 
    ? props.boxplotData.no.reduce((acc, val) => acc + val, 0) / props.boxplotData.no.length
    : 0;
  
  // 2. 计算所有人群的平均BMI和平均医保费用
  const avgBmi = props.scatterBmiData?.length 
    ? props.scatterBmiData.reduce((acc, val) => acc + val[0], 0) / props.scatterBmiData.length
    : 0;
  
  const avgChargesFromBmi = props.scatterBmiData?.length 
    ? props.scatterBmiData.reduce((acc, val) => acc + val[1], 0) / props.scatterBmiData.length
    : 0;
  
  // 3. 计算平均年龄
  const avgAge = props.ageHistData?.length 
    ? props.ageHistData.reduce((acc, val) => acc + val, 0) / props.ageHistData.length
    : 0;
  
  // 4. 获取最高和最低地区医保费用
  let maxRegionCharge = 0;
  let minRegionCharge = Infinity;
  let avgRegionCharge = 0;
  
  if (props.regionAvgData && Object.keys(props.regionAvgData).length > 0) {
    const regionValues = Object.values(props.regionAvgData);
    maxRegionCharge = Math.max(...regionValues);
    minRegionCharge = Math.min(...regionValues);
    avgRegionCharge = regionValues.reduce((acc, val) => acc + val, 0) / regionValues.length;
  }

  // 5. 计算年龄与医保费用相关性
  const ageChargeCorrelation = calculateAgeChargeCorrelation(props.scatterAgeData);

  // 6. 从相关性矩阵中提取BMI与医保费用的相关性
  const bmiChargeCorrelation = calculateFeatureCorrelation(props.correlationData);

  // 将所有数据标准化到0-100的范围内，便于雷达图展示
  const maxMedicalCost = Math.max(smokerCharges, nonSmokerCharges, avgChargesFromBmi, maxRegionCharge);
  
  const indicators = [
    { name: '吸烟者医保费用', max: maxMedicalCost * 1.2 },
    { name: '非吸烟者医保费用', max: maxMedicalCost * 1.2 },
    { name: '平均BMI指数', max: 40 }, // 正常BMI范围18.5-24.9，肥胖>30
    { name: '平均年龄', max: 65 }, // 假设数据集年龄范围
    { name: '地区医保费用差异', max: maxRegionCharge - minRegionCharge > 0 ? (maxRegionCharge - minRegionCharge) * 1.2 : 10000 },
    { name: '年龄-医保费用相关性', max: 1 }, // 相关性范围-1到1
    { name: 'BMI-医保费用相关性', max: 1 }, // 相关性范围-1到1
  ];

  // 更新指标说明
  indicatorExplanations.value = [
    { name: '吸烟者医保费用', value: formatNumber(smokerCharges, 'money') },
    { name: '非吸烟者医保费用', value: formatNumber(nonSmokerCharges, 'money') },
    { name: '平均BMI指数', value: formatNumber(avgBmi, 'decimal') },
    { name: '平均年龄', value: `${formatNumber(avgAge, 'decimal')}岁` },
    { name: '地区医保费用差异', value: formatNumber(maxRegionCharge - minRegionCharge, 'money') },
    { name: '年龄-医保费用相关性', value: formatNumber(Math.abs(ageChargeCorrelation), 'correlation') },
    { name: 'BMI-医保费用相关性', value: formatNumber(Math.abs(bmiChargeCorrelation), 'correlation') }
  ];

  const dataValues = [
    smokerCharges,
    nonSmokerCharges,
    avgBmi,
    avgAge,
    maxRegionCharge - minRegionCharge,
    Math.abs(ageChargeCorrelation),
    Math.abs(bmiChargeCorrelation)
  ];

  return {
    backgroundColor: 'transparent',
    tooltip: {
      trigger: 'item',
      formatter: function(params) {
        const index = params.dataIndex;
        const indicator = indicators[index];
        const value = dataValues[index];
        let formattedValue;
        
        if (index <= 1 || index === 4) {
          formattedValue = formatNumber(value, 'money');
        } else if (index === 2) {
          formattedValue = formatNumber(value, 'decimal');
        } else if (index === 3) {
          formattedValue = `${formatNumber(value, 'decimal')}岁`;
        } else {
          formattedValue = formatNumber(value, 'correlation');
        }
        
        return `<div style="font-weight:bold;color:${indicatorColors[index]}">${indicator.name}</div>
                <div>数值: ${formattedValue}</div>
                <div>占比: ${formatNumber((value / indicator.max) * 100, 'percent')}</div>`;
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
      show: false
    },
    radar: {
      indicator: indicators,
      center: ['50%', '50%'],
      radius: '70%',
      name: {
        textStyle: {
          color: '#fff',
          fontSize: 13,
          fontWeight: 'bold',
          backgroundColor: 'rgba(15, 37, 75, 0.8)',
          borderRadius: 3,
          padding: [5, 7]
        },
        formatter: function(name) {
          if (name.length > 8) {
            return name.substring(0, 8) + '...';
          }
          return name;
        }
      },
      splitArea: {
        areaStyle: {
          color: ['rgba(15, 110, 205, 0.03)', 'rgba(15, 110, 205, 0.05)', 
                  'rgba(15, 110, 205, 0.07)', 'rgba(15, 110, 205, 0.09)', 
                  'rgba(15, 110, 205, 0.11)']
        }
      },
      axisLine: {
        lineStyle: {
          color: 'rgba(15, 110, 205, 0.4)'
        }
      },
      splitLine: {
        show: false
      }
    },
    series: [
      {
        type: 'radar',
        data: [
          {
            value: dataValues,
            name: '医保数据综合分析',
            symbol: 'circle',
            symbolSize: 8,
            areaStyle: {
              color: {
                type: 'radial',
                x: 0.5,
                y: 0.5,
                r: 0.5,
                colorStops: [
                  { offset: 0, color: 'rgba(0, 255, 255, 0.8)' },
                  { offset: 1, color: 'rgba(51, 153, 255, 0.2)' }
                ]
              },
              shadowBlur: 15,
              shadowColor: 'rgba(0, 255, 255, 0.5)',
              opacity: 0.8
            },
            lineStyle: {
              width: 3,
              color: '#00FFFF',
              shadowBlur: 10,
              shadowColor: 'rgba(0, 255, 255, 0.8)'
            },
            itemStyle: {
              color: '#00FFFF',
              borderColor: '#fff',
              borderWidth: 2,
              shadowBlur: 10,
              shadowColor: 'rgba(0, 255, 255, 0.8)'
            },
            label: {
              show: true,
              formatter: function(params) {
                const index = params.dataIndex;
                if (index <= 1 || index === 4) {
                  return formatNumber(params.value, 'money');
                } else if (index === 2) {
                  return formatNumber(params.value, 'decimal');
                } else if (index === 3) {
                  return `${formatNumber(params.value, 'decimal')}岁`;
                } else {
                  return formatNumber(params.value, 'correlation');
                }
              },
              color: '#fff',
              backgroundColor: 'rgba(15, 37, 75, 0.7)',
              borderRadius: 3,
              padding: [3, 5],
              distance: 15,
              rotate: function(params) {
                // 根据不同位置调整标签旋转角度
                const index = params.dataIndex;
                if (index === 0) return -30;
                if (index === 1) return 30;
                if (index === 2) return 0;
                if (index === 3) return 0;
                if (index === 4) return 0;
                if (index === 5) return -30;
                if (index === 6) return 30;
                return 0;
              }
            }
          }
        ]
      }
    ]
  };
});

// 计算年龄与医保费用的相关性
function calculateAgeChargeCorrelation(data) {
  if (!data || data.length === 0) return 0;
  
  const ages = data.map(item => item[0]);
  const charges = data.map(item => item[1]);
  
  return pearsonCorrelation(ages, charges);
}

// 从相关性数据中提取BMI与医保费用的相关性
function calculateFeatureCorrelation(data) {
  if (!data || data.length === 0) return 0;
  
  // 相关性矩阵数据：age, bmi, children, charges
  const bmi = data.map(item => item[1]);
  const charges = data.map(item => item[3]);
  
  return pearsonCorrelation(bmi, charges);
}

// 计算皮尔逊相关系数
function pearsonCorrelation(x, y) {
  if (!x || !y || x.length === 0 || y.length === 0) return 0;
  
  const n = Math.min(x.length, y.length);
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
</script>

<style scoped>
.chart-wrapper {
  height: 100%;
  width: 100%;
  display: flex;
  flex-direction: column;
  border: 0 none !important;
  outline: 0 none !important;
  box-shadow: none !important;
  background-clip: content-box;
}

.chart-title {
  height: 36px;
  line-height: 36px;
  padding: 0 15px;
  font-size: 16px;
  color: #00FFFF;
  border: none;
  border-bottom: none;
  background-color: transparent;
  font-weight: bold;
  display: flex;
  justify-content: center;
}

.chart-container {
  flex: 3;
  width: 100%;
  position: relative;
  border: 0 none !important;
}

.chart {
  width: 100%;
  height: 100%;
  border: 0 none !important;
}

.chart-indicators {
  flex: 0.8;
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 6px;
  padding: 6px;
  background-color: transparent;
  border: none;
}

.indicator-item {
  display: flex;
  align-items: center;
  background-color: rgba(15, 37, 75, 0.3);
  border-radius: 4px;
  padding: 5px 10px;
  min-width: 140px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.indicator-color {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  margin-right: 8px;
}

.indicator-text {
  display: flex;
  flex-direction: column;
}

.indicator-name {
  font-size: 12px;
  color: #7eb6ff;
}

.indicator-value {
  font-size: 14px;
  font-weight: bold;
  color: #fff;
}
</style> 