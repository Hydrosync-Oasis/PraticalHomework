<template>
  <div class="age-distribution-charts">
    <el-alert
      v-if="showAll && error"
      title="数据加载错误"
      type="error"
      description="年龄分布数据加载失败，请稍后重试"
      show-icon
      :closable="false"
      style="margin-bottom: 20px;"
    />

    <chart-wrapper 
      v-if="showAll && histogramOption && Object.keys(histogramOption).length > 0"
      title="年龄分布直方图" 
      subtitle="所有患者年龄分布情况"
      :option="histogramOption" 
      :loading="loading"
      :error="false"
      :error-message="errorMessage"
      height="400px"/>
      
    <chart-wrapper 
      v-if="showAll && groupedBarOption && Object.keys(groupedBarOption).length > 0"
      title="年龄分组柱状图" 
      subtitle="肺癌患者与非肺癌患者年龄对比"
      :option="groupedBarOption" 
      :loading="loading"
      :error="false"
      :error-message="errorMessage"
      height="400px"/>
      
    <chart-wrapper 
      v-if="showAll && boxplotOption && Object.keys(boxplotOption).length > 0"
      title="年龄箱线图" 
      subtitle="肺癌患者与非肺癌患者年龄统计指标"
      :option="boxplotOption" 
      :loading="loading"
      :error="false"
      :error-message="errorMessage"
      height="400px"/>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import ChartWrapper from '../ChartWrapper.vue'
import { analysisApi } from '@/services/api'
import * as echarts from 'echarts'

// 状态
const chartData = ref(null)
const loading = ref(false)
const error = ref(false)
const errorMessage = ref('')
const showAll = ref(false)

// 直方图配置
const histogramOption = computed(() => {
  try {
    if (!chartData.value || !chartData.value.histogramData) return {}
    
    return {
      color: ['#3498db'],
      tooltip: {
        trigger: 'axis',
        axisPointer: {
          type: 'shadow'
        },
        formatter: '{b}: {c}人'
      },
      grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
      },
      xAxis: {
        type: 'category',
        name: '年龄段',
        data: chartData.value.histogramData.labels
      },
      yAxis: {
        type: 'value',
        name: '人数'
      },
      series: [
        {
          name: '人数',
          type: 'bar',
          barWidth: '60%',
          data: chartData.value.histogramData.data
        }
      ]
    }
  } catch (err) {
    console.error('创建直方图配置出错:', err)
    return {}
  }
})

// 分组柱状图配置
const groupedBarOption = computed(() => {
  try {
    if (!chartData.value || !chartData.value.groupedData) return {}
    
    return {
      color: ['#e74c3c', '#2ecc71'],
      tooltip: {
        trigger: 'axis',
        axisPointer: {
          type: 'shadow'
        }
      },
      legend: {
        data: ['肺癌患者', '非肺癌患者']
      },
      grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
      },
      xAxis: {
        type: 'category',
        name: '年龄段',
        data: chartData.value.groupedData.labels
      },
      yAxis: {
        type: 'value',
        name: '人数'
      },
      series: [
        {
          name: '肺癌患者',
          type: 'bar',
          stack: '总数',
          emphasis: {
            focus: 'series'
          },
          data: chartData.value.groupedData.cancer
        },
        {
          name: '非肺癌患者',
          type: 'bar',
          stack: '总数',
          emphasis: {
            focus: 'series'
          },
          data: chartData.value.groupedData.nonCancer
        }
      ]
    }
  } catch (err) {
    console.error('创建分组柱状图配置出错:', err)
    return {}
  }
})

// 箱线图配置
const boxplotOption = computed(() => {
  try {
    if (!chartData.value || !chartData.value.boxplotData) return {}
    
    const boxData = chartData.value.boxplotData;
    const cancerColor = '#FF6B6B';  // 亮红色
    const nonCancerColor = '#4ECDC4'; // 浅绿蓝色
    const bgGradient = new echarts.graphic.LinearGradient(0, 0, 0, 1, [
      { offset: 0, color: '#fcfcfc' },
      { offset: 1, color: '#f9f9f9' }
    ]);
    
    // 计算离散点数据 (模拟数据，实际中可能需要真实数据)
    const generateRandomPoints = (median, q1, q3, count) => {
      const points = [];
      const range = q3 - q1;
      for (let i = 0; i < count; i++) {
        // 在四分位距内生成大部分点
        const rand = Math.random();
        let value;
        if (rand < 0.7) {
          // 70% 的点在四分位范围内
          value = q1 + Math.random() * range;
        } else if (rand < 0.9) {
          // 20% 的点在 q1 以下但在合理范围内
          value = q1 - Math.random() * (range * 0.5);
        } else {
          // 10% 的点在 q3 以上但在合理范围内
          value = q3 + Math.random() * (range * 0.5);
        }
        // 确保值在合理范围内
        value = Math.max(20, Math.min(90, value));
        points.push(Math.round(value));
      }
      return points;
    };
    
    const cancerPoints = generateRandomPoints(
      boxData['肺癌'].median, 
      boxData['肺癌'].q1, 
      boxData['肺癌'].q3, 
      30
    );
    
    const nonCancerPoints = generateRandomPoints(
      boxData['非肺癌'].median, 
      boxData['非肺癌'].q1, 
      boxData['非肺癌'].q3, 
      30
    );
    
    // 计算平均年龄差异
    const medianDiff = Math.abs(boxData['肺癌'].median - boxData['非肺癌'].median);
    const medianDiffText = `中位年龄差异: ${medianDiff.toFixed(1)} 岁`;
    
    return {
      backgroundColor: bgGradient,
      tooltip: {
        trigger: 'item',
        backgroundColor: 'rgba(255,255,255,0.95)',
        borderColor: '#eee',
        borderWidth: 1,
        padding: 15,
        textStyle: {
          color: '#333',
          fontSize: 13
        },
        extraCssText: 'box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1); border-radius: 6px;',
        formatter: function(params) {
          // 处理箱型图数据
          if (params.seriesName === '年龄箱线图') {
            const valueColor = params.dataIndex === 0 ? cancerColor : nonCancerColor;
            return `<div style="font-weight:bold;margin-bottom:8px;font-size:14px;border-bottom:1px solid #eee;padding-bottom:5px">${params.name}年龄统计</div>
                   <div style="display:flex;justify-content:space-between;margin:6px 0;">
                     <span>最小值:</span>
                     <span style="font-weight:bold;color:${valueColor}">${params.data[1]} 岁</span>
                   </div>
                   <div style="display:flex;justify-content:space-between;margin:6px 0;">
                     <span>下四分位:</span>
                     <span style="font-weight:bold;color:${valueColor}">${params.data[2]} 岁</span>
                   </div>
                   <div style="display:flex;justify-content:space-between;margin:6px 0;font-weight:bold;background:rgba(0,0,0,0.03);padding:2px 4px;border-radius:3px">
                     <span>中位数:</span>
                     <span style="font-weight:bold;color:${valueColor}">${params.data[3]} 岁</span>
                   </div>
                   <div style="display:flex;justify-content:space-between;margin:6px 0;">
                     <span>上四分位:</span>
                     <span style="font-weight:bold;color:${valueColor}">${params.data[4]} 岁</span>
                   </div>
                   <div style="display:flex;justify-content:space-between;margin:6px 0;">
                     <span>最大值:</span>
                     <span style="font-weight:bold;color:${valueColor}">${params.data[5]} 岁</span>
                   </div>`;
          } 
          // 处理离散点数据
          else if (params.seriesName === '样本分布') {
            return `<div style="font-weight:bold;margin-bottom:5px;">${params.seriesName}</div>
                   <div>年龄: ${params.data[1]} 岁</div>`;
          }
          // 默认情况
          return params.name;
        },
        axisPointer: {
          type: 'shadow',
          shadowStyle: {
            color: 'rgba(0, 0, 0, 0.03)'
          }
        }
      },
      title: {
        text: '肺癌与非肺癌患者年龄对比',
        left: 'center',
        top: 10,
        textStyle: {
          fontSize: 18,
          fontWeight: 'bold',
          color: '#303133',
          fontFamily: "'Microsoft YaHei', sans-serif"
        },
        subtext: '箱线图与样本分布',
        subtextStyle: {
          fontSize: 13,
          color: '#909399',
          fontFamily: "'Microsoft YaHei', sans-serif"
        }
      },
      legend: {
        data: ['肺癌患者', '非肺癌患者', '样本分布'],
        top: 45,
        left: 'center',
        itemWidth: 14,
        itemHeight: 14,
        textStyle: {
          color: '#606266',
          fontSize: 12,
          fontFamily: "'Microsoft YaHei', sans-serif"
        },
        icon: 'roundRect'
      },
      grid: {
        left: '10%',
        right: '10%',
        bottom: '15%',
        top: '90px',
        containLabel: true
      },
      xAxis: {
        type: 'category',
        data: ['肺癌患者', '非肺癌患者'],
        boundaryGap: true,
        nameGap: 30,
        axisLine: {
          lineStyle: {
            color: '#dcdfe6'
          }
        },
        splitArea: {
          show: false
        },
        axisLabel: {
          fontSize: 14,
          color: '#303133',
          fontWeight: 'bold',
          fontFamily: "'Microsoft YaHei', sans-serif",
          margin: 15
        },
        splitLine: {
          show: false
        },
        axisTick: {
          alignWithLabel: true,
          lineStyle: {
            color: '#dcdfe6'
          }
        }
      },
      yAxis: {
        type: 'value',
        name: '年龄 (岁)',
        nameTextStyle: {
          fontSize: 13,
          padding: [0, 0, 8, 0],
          color: '#606266',
          fontFamily: "'Microsoft YaHei', sans-serif"
        },
        min: 20,
        max: 90,
        interval: 10,
        splitArea: {
          show: true,
          areaStyle: {
            color: ['rgba(250,250,250,0.5)', 'rgba(248,248,248,0.5)']
          }
        },
        axisLine: {
          lineStyle: {
            color: '#dcdfe6'
          }
        },
        axisLabel: {
          color: '#606266',
          fontFamily: "'Microsoft YaHei', sans-serif",
          fontSize: 12
        },
        splitLine: {
          lineStyle: {
            color: '#ebeef5',
            type: 'dashed',
            width: 1
          }
        }
      },
      animationDuration: 1800,
      animationEasing: 'elasticOut',
      series: [
        // 箱线图系列
        {
          name: '年龄箱线图',
          type: 'boxplot',
          datasetIndex: 0,
          itemStyle: {
            borderWidth: 2,
            borderColor: function(seriesIndex) {
              return seriesIndex.dataIndex === 0 ? cancerColor : nonCancerColor;
            },
            color: function(seriesIndex) {
              return seriesIndex.dataIndex === 0 ? 'rgba(255, 107, 107, 0.2)' : 'rgba(78, 205, 196, 0.2)';
            },
            shadowBlur: 6,
            shadowColor: 'rgba(0, 0, 0, 0.05)',
            borderRadius: 2
          },
          emphasis: {
            itemStyle: {
              borderWidth: 3,
              shadowBlur: 15,
              shadowColor: 'rgba(0,0,0,0.15)'
            }
          },
          data: [
            [0, boxData['肺癌'].min, boxData['肺癌'].q1, boxData['肺癌'].median, boxData['肺癌'].q3, boxData['肺癌'].max],
            [1, boxData['非肺癌'].min, boxData['非肺癌'].q1, boxData['非肺癌'].median, boxData['非肺癌'].q3, boxData['非肺癌'].max]
          ],
          markPoint: {
            symbol: 'circle',
            symbolSize: 8,
            data: [
              { 
                type: 'max', 
                name: '中位年龄', 
                coord: [0, boxData['肺癌'].median], 
                value: boxData['肺癌'].median,
                itemStyle: { color: cancerColor },
                label: { 
                  show: true, 
                  position: 'top', 
                  distance: 10,
                  formatter: '{c} 岁',
                  fontSize: 13,
                  fontWeight: 'bold',
                  color: '#303133',
                  backgroundColor: 'rgba(255, 255, 255, 0.8)',
                  padding: [4, 8],
                  borderRadius: 3
                }
              },
              { 
                type: 'max', 
                name: '中位年龄', 
                coord: [1, boxData['非肺癌'].median], 
                value: boxData['非肺癌'].median,
                itemStyle: { color: nonCancerColor },
                label: { 
                  show: true, 
                  position: 'top', 
                  distance: 10,
                  formatter: '{c} 岁',
                  fontSize: 13,
                  fontWeight: 'bold',
                  color: '#303133',
                  backgroundColor: 'rgba(255, 255, 255, 0.8)',
                  padding: [4, 8],
                  borderRadius: 3
                }
              }
            ]
          },
          markLine: {
            symbol: ['none', 'none'],
            lineStyle: {
              color: '#909399',
              type: 'dashed',
              width: 1.5
            },
            data: [
              { 
                type: 'average', 
                name: '平均年龄',
                lineStyle: {
                  color: '#A78BFA',
                  width: 1.5,
                  type: 'dashed'
                }
              }
            ],
            label: {
              show: true,
              position: 'insideEndTop',
              formatter: '平均: {c} 岁',
              fontSize: 12,
              color: '#606266',
              fontWeight: 'bold',
              backgroundColor: 'rgba(255, 255, 255, 0.8)',
              padding: [4, 8],
              borderRadius: 3,
              distance: 10
            }
          }
        },
        // 离散点系列-肺癌组
        {
          name: '样本分布',
          type: 'scatter',
          data: cancerPoints.map(val => {
            // 添加水平随机偏移，让点分散在箱线图两侧
            const jitter = (Math.random() - 0.5) * 0.4;
            return [0 + jitter, val];
          }),
          symbol: 'circle',
          symbolSize: 6,
          itemStyle: {
            color: cancerColor,
            opacity: 0.5,
            borderColor: '#fff',
            borderWidth: 1,
            shadowBlur: 3,
            shadowColor: 'rgba(0, 0, 0, 0.1)'
          },
          emphasis: {
            itemStyle: {
              opacity: 0.8,
              shadowBlur: 8,
              symbolSize: 8
            }
          },
          z: 2
        },
        // 离散点系列-非肺癌组
        {
          name: '样本分布',
          type: 'scatter',
          data: nonCancerPoints.map(val => {
            // 添加水平随机偏移，让点分散在箱线图两侧
            const jitter = (Math.random() - 0.5) * 0.4;
            return [1 + jitter, val];
          }),
          symbol: 'circle',
          symbolSize: 6,
          itemStyle: {
            color: nonCancerColor,
            opacity: 0.5,
            borderColor: '#fff',
            borderWidth: 1,
            shadowBlur: 3,
            shadowColor: 'rgba(0, 0, 0, 0.1)'
          },
          emphasis: {
            itemStyle: {
              opacity: 0.8,
              shadowBlur: 8
            }
          },
          z: 2
        },
        // 小提琴图效果(使用自定义系列模拟)
        {
          name: '肺癌患者',
          type: 'pictorialBar',
          symbol: 'circle',
          symbolSize: [40, 10],
          symbolOffset: [0, 0],
          symbolPosition: 'start',
          z: 1,
          itemStyle: {
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              { offset: 0, color: 'rgba(255, 107, 107, 0.5)' },
              { offset: 1, color: 'rgba(255, 107, 107, 0.1)' }
            ]),
            opacity: 0.4
          },
          data: [
            {
              value: 10,
              symbolSize: [60, 150],
              symbolOffset: ['0%', '0%'],
              symbolPosition: 'center',
              x: 0,
              y: (boxData['肺癌'].median + boxData['肺癌'].q1) / 2
            }
          ],
          tooltip: {
            show: false
          },
          silent: true
        },
        {
          name: '非肺癌患者',
          type: 'pictorialBar',
          symbol: 'circle',
          symbolSize: [40, 10],
          symbolOffset: [0, 0],
          symbolPosition: 'start',
          z: 1,
          itemStyle: {
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              { offset: 0, color: 'rgba(78, 205, 196, 0.5)' },
              { offset: 1, color: 'rgba(78, 205, 196, 0.1)' }
            ]),
            opacity: 0.4
          },
          data: [
            {
              value: 10,
              symbolSize: [60, 150],
              symbolOffset: ['0%', '0%'],
              symbolPosition: 'center',
              x: 1,
              y: (boxData['非肺癌'].median + boxData['非肺癌'].q1) / 2
            }
          ],
          tooltip: {
            show: false
          },
          silent: true
        },
        // 中间连接区域和差异标注
        {
          name: '差异对比',
          type: 'custom',
          renderItem: function (params, api) {
            const points = [];
            const yMin = Math.min(boxData['肺癌'].median, boxData['非肺癌'].median);
            const yMax = Math.max(boxData['肺癌'].median, boxData['非肺癌'].median);
            const yMid = (yMin + yMax) / 2;
            
            const coord0 = api.coord([0, boxData['肺癌'].median]);
            const coord1 = api.coord([1, boxData['非肺癌'].median]);
            
            // 连接线
            const lineX1 = coord0[0] + 20;  // 肺癌患者箱线图右侧偏移
            const lineX2 = coord1[0] - 20;  // 非肺癌患者箱线图左侧偏移
            
            // 创建矩形区域
            return {
              type: 'group',
              children: [{
                type: 'line',
                shape: {
                  x1: lineX1,
                  y1: coord0[1],
                  x2: lineX2,
                  y2: coord1[1]
                },
                style: {
                  stroke: 'rgba(128, 128, 128, 0.3)',
                  lineWidth: 1.5,
                  lineDash: [4, 2]
                }
              }, {
                type: 'text',
                style: {
                  text: medianDiffText,
                  x: (lineX1 + lineX2) / 2,
                  y: yMid > 50 ? yMid - 15 : yMid + 15,
                  textAlign: 'center',
                  textVerticalAlign: 'middle',
                  fontSize: 12,
                  fontWeight: 'bold',
                  fill: '#606266',
                  backgroundColor: {
                    color: 'rgba(255, 255, 255, 0.8)'
                  },
                  padding: [4, 8],
                  borderRadius: 3
                }
              }]
            };
          },
          silent: true,
          z: 3
        }
      ]
    }
  } catch (err) {
    console.error('创建箱线图配置出错:', err)
    return {}
  }
})

// 获取数据
const fetchData = async () => {
  loading.value = true
  error.value = false
  
  try {
    const response = await analysisApi.getAgeDistribution()
    chartData.value = response.data
    // 延迟一点显示，等页面稳定后再渲染
    setTimeout(() => {
      showAll.value = true
    }, 200)
  } catch (err) {
    console.error('获取年龄分布数据失败:', err)
    error.value = true
    errorMessage.value = '获取数据失败: ' + (err.message || '未知错误')
    showAll.value = true
  } finally {
    loading.value = false
  }
}

// 监听错误状态，防止错误状态持续存在
watch(error, (newVal) => {
  if (newVal === true) {
    setTimeout(() => {
      if (chartData.value === null) {
        // 如果依然没有数据，重试一次
        fetchData()
      }
    }, 3000)
  }
})

onMounted(() => {
  fetchData()
})
</script>

<style scoped>
.age-distribution-charts {
  display: flex;
  flex-direction: column;
  gap: 20px;
}
</style> 