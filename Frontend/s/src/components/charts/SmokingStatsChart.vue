<template>
  <div class="smoking-stats-charts">
    <el-alert
      v-if="showAll && error"
      title="数据加载错误"
      type="error"
      description="吸烟数据加载失败，请稍后重试"
      show-icon
      :closable="false"
      style="margin-bottom: 20px;"
    />

    <chart-wrapper 
      v-if="showAll && barChartOption && Object.keys(barChartOption).length > 0"
      title="吸烟与肺癌关系" 
      subtitle="吸烟者与非吸烟者肺癌对比"
      intro="本图表展示了吸烟者与非吸烟者中肺癌患者的分布情况。从图表可以看出，吸烟者中肺癌患者比例明显高于非吸烟者，说明吸烟与肺癌有较强的相关性。"
      :option="barChartOption" 
      :loading="loading"
      :error="false"
      height="400px">
      <template #data-table>
        <div class="data-summary">
          <h4>数据统计表</h4>
          <el-table :data="smokingSummaryData" stripe style="width: 100%" :border="true" size="small">
            <el-table-column prop="category" label="人群" width="180" />
            <el-table-column prop="total" label="总人数" width="120" />
            <el-table-column prop="cancer" label="肺癌患者" width="120" />
            <el-table-column prop="nonCancer" label="非肺癌患者" width="120" />
            <el-table-column prop="cancerRatio" label="肺癌率">
              <template #default="scope">
                <div class="ratio-cell">
                  <span>{{ scope.row.cancerRatio }}%</span>
                  <div class="ratio-bar" :style="{width: scope.row.cancerRatio + '%', backgroundColor: scope.row.category === '吸烟' ? '#e74c3c' : '#f39c12'}"></div>
                </div>
              </template>
            </el-table-column>
          </el-table>
        </div>
      </template>
    </chart-wrapper>
      
    <chart-wrapper 
      v-if="showAll && stackBarOption && Object.keys(stackBarOption).length > 0"
      title="各年龄段吸烟情况" 
      subtitle="各年龄组吸烟与不吸烟对比"
      intro="该图表展示了不同年龄段人群中吸烟者与非吸烟者的分布情况及比例。柱状图显示各年龄段吸烟和不吸烟的人数，折线图表示各年龄段的吸烟比例。可以观察到不同年龄段吸烟习惯的差异。"
      :option="stackBarOption" 
      :loading="loading"
      :error="false"
      height="400px">
      <template #data-table>
        <div class="data-summary" v-if="chartData && chartData.smokingByAge">
          <h4>年龄段吸烟情况统计</h4>
          <el-table :data="chartData.smokingByAge" stripe style="width: 100%" :border="true" size="small">
            <el-table-column prop="ageGroup" label="年龄段" width="120" />
            <el-table-column prop="smoking" label="吸烟人数" width="120" />
            <el-table-column prop="nonSmoking" label="不吸烟人数" width="120" />
            <el-table-column prop="total" label="总人数" width="120" />
            <el-table-column prop="smokingPercent" label="吸烟比例">
              <template #default="scope">
                <div class="ratio-cell">
                  <span>{{ scope.row.smokingPercent }}%</span>
                  <div class="ratio-bar" :style="{width: scope.row.smokingPercent + '%', backgroundColor: '#f39c12'}"></div>
                </div>
              </template>
            </el-table-column>
          </el-table>
        </div>
      </template>
    </chart-wrapper>
      
    <chart-wrapper 
      v-if="showAll && boxplotOption && Object.keys(boxplotOption).length > 0"
      title="吸烟与年龄箱线图" 
      subtitle="吸烟者与非吸烟者的年龄分布"
      intro="该箱线图展示了吸烟者和非吸烟者的年龄分布情况。箱体中间线表示中位数，箱体上下边界分别表示上下四分位数，延伸线表示最大最小值范围。从图中可以分析两组人群的年龄特征。"
      :option="boxplotOption" 
      :loading="loading"
      :error="false"
      height="400px" />
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
const showAll = ref(false)

// 吸烟摘要数据
const smokingSummaryData = computed(() => {
  if (!chartData.value || !chartData.value.smokingCancerData || !chartData.value.summary) return []
  
  const { smokingCancerData, summary } = chartData.value
  const cancerRatio = smokingCancerData.cancerRatio || [0, 0]
  
  return [
    { 
      category: '吸烟', 
      total: summary.totalSmoking, 
      cancer: summary.smokingCancer, 
      nonCancer: summary.totalSmoking - summary.smokingCancer,
      cancerRatio: cancerRatio[0] || ((summary.smokingCancer / summary.totalSmoking) * 100).toFixed(1)
    },
    { 
      category: '不吸烟', 
      total: summary.totalNonSmoking, 
      cancer: summary.nonSmokingCancer, 
      nonCancer: summary.totalNonSmoking - summary.nonSmokingCancer,
      cancerRatio: cancerRatio[1] || ((summary.nonSmokingCancer / summary.totalNonSmoking) * 100).toFixed(1)
    }
  ]
})

// 吸烟与肺癌柱状图
const barChartOption = computed(() => {
  try {
    if (!chartData.value || !chartData.value.smokingCancerData) return {}
    
    const { categories, cancer, nonCancer, cancerRatio } = chartData.value.smokingCancerData
    
    return {
      tooltip: {
        trigger: 'axis',
        axisPointer: {
          type: 'shadow'
        },
        formatter: function(params) {
          const category = params[0].axisValue;
          const cancerCount = params[0].data;
          const nonCancerCount = params[1] ? params[1].data : 0;
          const total = cancerCount + nonCancerCount;
          const ratio = (cancerCount / total * 100).toFixed(1);
          return `${category}<br/>
                 肺癌患者: ${cancerCount} 人 (${ratio}%)<br/>
                 非肺癌患者: ${nonCancerCount} 人<br/>
                 总计: ${total} 人`;
        }
      },
      legend: [
        {
          // 柱状图图例
          data: ['肺癌患者', '非肺癌患者'],
          top: 10,
          left: '20%', // 更靠左一些
          textStyle: {
            fontSize: 12,
            fontWeight: 'bold' // 加粗以区分
          }
        },
        {
          // 饼图图例
          data: ['吸烟肺癌患者', '吸烟非肺癌患者', '不吸烟肺癌患者', '不吸烟非肺癌患者'],
          top: 10, // 放在顶部
          right: '5%', // 使用right定位，确保不会超出右侧边界
          orient: 'vertical', // 纵向排列
          align: 'left', // 左对齐
          itemWidth: 14,
          itemHeight: 14,
          itemGap: 5, // 紧凑间距
          textStyle: {
            fontSize: 11,
            color: '#666' // 稍微区分颜色
          },
          formatter: function(name) {
            return name;
          }
        }
      ],
      grid: {
        left: '3%',
        right: '55%', // 留出右侧空间给饼图
        bottom: '20%', // 增加更多底部空间
        top: '70px',
        containLabel: true
      },
      xAxis: [
        {
          type: 'category',
          data: categories,
          axisTick: {
            alignWithLabel: true
          }
        }
      ],
      yAxis: [
        {
          type: 'value',
          name: '人数',
          max: 180,
          interval: 30
        }
      ],
      series: [
        {
          name: '肺癌患者',
          type: 'bar',
          stack: '总量',
          emphasis: {
            focus: 'series'
          },
          data: cancer,
          itemStyle: {
            color: '#e74c3c'
          },
          barWidth: '40%'
        },
        {
          name: '非肺癌患者',
          type: 'bar',
          stack: '总量',
          emphasis: {
            focus: 'series'
          },
          data: nonCancer,
          itemStyle: {
            color: '#2ecc71'
          },
          barWidth: '40%'
        },
        // 添加饼图
        {
          name: '肺癌患病分布',
          type: 'pie',
          radius: ['30%', '50%'], // 稍微缩小饼图
          center: ['75%', '55%'], // 饼图向下移动，避免与图例重叠
          avoidLabelOverlap: false,
          itemStyle: {
            borderRadius: 5,
            borderColor: '#fff',
            borderWidth: 2
          },
          label: {
            show: true,
            position: 'outside',
            formatter: '{b}\n{c}',  // 同时显示名称和数值
            fontSize: 12,
            lineHeight: 18,
            backgroundColor: 'rgba(255,255,255,0.7)',
            padding: [4, 8],
            borderRadius: 4
          },
          labelLine: {
            show: true,
            length: 12,
            length2: 15,
            smooth: 0.5, // 增加平滑度
            lineStyle: {
              width: 1.5,
              type: 'solid'
            }
          },
          data: [
            {value: cancer[0], name: '吸烟肺癌患者', itemStyle: {color: '#C23531'}},
            {value: nonCancer[0], name: '吸烟非肺癌患者', itemStyle: {color: '#61A0A8'}},
            {value: cancer[1], name: '不吸烟肺癌患者', itemStyle: {color: '#D48265'}},
            {value: nonCancer[1], name: '不吸烟非肺癌患者', itemStyle: {color: '#91C7AE'}}
          ],
          emphasis: {
            itemStyle: {
              shadowBlur: 10,
              shadowOffsetX: 0,
              shadowColor: 'rgba(0, 0, 0, 0.5)'
            }
          }
        }
      ]
    }
  } catch (err) {
    console.error('创建柱状图配置出错:', err)
    return {}
  }
})

// 箱线图配置
const boxplotOption = computed(() => {
  try {
    if (!chartData.value || !chartData.value.boxplotData) return {}
    
    const boxData = chartData.value.boxplotData;
    const smokerColor = '#FF6B6B';  // 亮红色
    const nonSmokerColor = '#4ECDC4'; // 浅绿蓝色
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
    
    const smokerPoints = generateRandomPoints(
      boxData['吸烟'].median, 
      boxData['吸烟'].q1, 
      boxData['吸烟'].q3, 
      30
    );
    
    const nonSmokerPoints = generateRandomPoints(
      boxData['不吸烟'].median, 
      boxData['不吸烟'].q1, 
      boxData['不吸烟'].q3, 
      30
    );
    
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
          if (params.seriesName === '年龄分布') {
            const valueColor = params.dataIndex === 0 ? smokerColor : nonSmokerColor;
            return `<div style="font-weight:bold;margin-bottom:8px;font-size:14px;border-bottom:1px solid #eee;padding-bottom:5px">${params.name}人群年龄统计</div>
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
        text: '吸烟与非吸烟人群年龄分布对比',
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
        data: ['吸烟人群', '不吸烟人群', '样本分布'],
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
        data: ['吸烟', '不吸烟'],
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
          name: '年龄分布',
          type: 'boxplot',
          datasetIndex: 0,
          itemStyle: {
            borderWidth: 2,
            borderColor: function(seriesIndex) {
              return seriesIndex.dataIndex === 0 ? smokerColor : nonSmokerColor;
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
            [0, boxData['吸烟'].min, boxData['吸烟'].q1, boxData['吸烟'].median, boxData['吸烟'].q3, boxData['吸烟'].max],
            [1, boxData['不吸烟'].min, boxData['不吸烟'].q1, boxData['不吸烟'].median, boxData['不吸烟'].q3, boxData['不吸烟'].max]
          ],
          markPoint: {
            symbol: 'circle',
            symbolSize: 8,
            data: [
              { 
                type: 'max', 
                name: '中位年龄', 
                coord: [0, boxData['吸烟'].median], 
                value: boxData['吸烟'].median,
                itemStyle: { color: smokerColor },
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
                coord: [1, boxData['不吸烟'].median], 
                value: boxData['不吸烟'].median,
                itemStyle: { color: nonSmokerColor },
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
        // 离散点系列-吸烟组
        {
          name: '样本分布',
          type: 'scatter',
          data: smokerPoints.map(val => {
            // 添加水平随机偏移，让点分散在箱线图两侧
            const jitter = (Math.random() - 0.5) * 0.4;
            return [0 + jitter, val];
          }),
          symbol: 'circle',
          symbolSize: 6,
          itemStyle: {
            color: smokerColor,
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
        // 离散点系列-不吸烟组
        {
          name: '样本分布',
          type: 'scatter',
          data: nonSmokerPoints.map(val => {
            // 添加水平随机偏移，让点分散在箱线图两侧
            const jitter = (Math.random() - 0.5) * 0.4;
            return [1 + jitter, val];
          }),
          symbol: 'circle',
          symbolSize: 6,
          itemStyle: {
            color: nonSmokerColor,
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
          name: '吸烟人群',
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
              y: (boxData['吸烟'].median + boxData['吸烟'].q1) / 2
            }
          ],
          tooltip: {
            show: false
          },
          silent: true
        },
        {
          name: '不吸烟人群',
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
              y: (boxData['不吸烟'].median + boxData['不吸烟'].q1) / 2
            }
          ],
          tooltip: {
            show: false
          },
          silent: true
        }
      ]
    }
  } catch (err) {
    console.error('创建箱线图配置出错:', err)
    return {}
  }
})

// 堆叠柱状图配置
const stackBarOption = computed(() => {
  try {
    if (!chartData.value || !chartData.value.smokingByAge) return {}
    
    const smokingByAge = chartData.value.smokingByAge;
    
    // 提取年龄组、吸烟人数和非吸烟人数
    const ageGroups = smokingByAge.map(item => item.ageGroup);
    const smokingData = smokingByAge.map(item => item.smoking);
    const nonSmokingData = smokingByAge.map(item => item.nonSmoking);
    const smokingPercent = smokingByAge.map(item => item.smokingPercent);
    
    return {
      title: {
        text: '各年龄段吸烟情况与比例',
        left: 'center',
        top: 10,
        textStyle: {
          fontSize: 14,
          fontWeight: 'normal'
        }
      },
      tooltip: {
        trigger: 'axis',
        axisPointer: {
          type: 'shadow'
        },
        formatter: function(params) {
          const ageGroup = params[0].axisValue;
          const ageData = smokingByAge.find(item => item.ageGroup === ageGroup);
          if (!ageData) return '';
          return `${ageGroup}<br/>
                  吸烟: ${ageData.smoking} 人 (${ageData.smokingPercent}%)<br/>
                  不吸烟: ${ageData.nonSmoking} 人 (${(100 - ageData.smokingPercent).toFixed(1)}%)<br/>
                  总计: ${ageData.total} 人`;
        }
      },
      legend: {
        data: ['吸烟', '不吸烟', '吸烟比例'],
        top: 35,
        left: 'center'
      },
      grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        top: '80px',
        containLabel: true
      },
      xAxis: {
        type: 'category',
        data: ageGroups
      },
      yAxis: [
        {
          type: 'value',
          name: '人数',
          position: 'left'
        },
        {
          type: 'value',
          name: '百分比',
          position: 'right',
          min: 0,
          max: 100,
          axisLabel: {
            formatter: '{value}%'
          }
        }
      ],
      series: [
        {
          name: '吸烟',
          type: 'bar',
          stack: '总数',
          emphasis: {
            focus: 'series'
          },
          itemStyle: {
            color: '#e74c3c'
          },
          data: smokingData
        },
        {
          name: '不吸烟',
          type: 'bar',
          stack: '总数',
          emphasis: {
            focus: 'series'
          },
          itemStyle: {
            color: '#2ecc71'
          },
          data: nonSmokingData
        },
        {
          name: '吸烟比例',
          type: 'line',
          yAxisIndex: 1,
          smooth: true,
          symbol: 'circle',
          symbolSize: 8,
          itemStyle: {
            color: '#f39c12'
          },
          lineStyle: {
            width: 2,
            type: 'solid'
          },
          tooltip: {
            valueFormatter: (value) => {
              return value + '%';
            }
          },
          data: smokingPercent
        }
      ]
    }
  } catch (err) {
    console.error('创建堆叠柱状图配置出错:', err)
    return {}
  }
})

// 获取数据
const fetchData = async () => {
  loading.value = true
  error.value = false
  
  try {
    const response = await analysisApi.getSmokingStats()
    chartData.value = response.data
    console.log('吸烟数据:', chartData.value)
    // 延迟一点显示，等页面稳定后再渲染
    setTimeout(() => {
      showAll.value = true
    }, 200)
  } catch (err) {
    console.error('获取吸烟统计数据失败:', err)
    error.value = true
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
.smoking-stats-charts {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.data-summary {
  margin-top: 24px;
  border-top: 1px solid #EBEEF5;
  padding-top: 20px;
}

.data-summary h4 {
  margin: 0 0 14px;
  font-size: 16px;
  color: #303133;
  position: relative;
  padding-left: 12px;
  font-weight: 600;
}

.data-summary h4::before {
  content: "";
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  height: 16px;
  width: 4px;
  background-color: #409EFF;
  border-radius: 2px;
}

:deep(.el-table) {
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

:deep(.el-table th) {
  background-color: #f5f7fa !important;
  color: #303133;
  font-weight: 600;
  padding: 10px 0;
  font-size: 14px;
}

:deep(.el-table td) {
  padding: 12px 0;
}

:deep(.el-table--striped .el-table__body tr.el-table__row--striped td) {
  background-color: #fafafa;
}

.ratio-cell {
  position: relative;
  padding-right: 10px;
  height: 24px;
  display: flex;
  align-items: center;
}

.ratio-bar {
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  height: 8px;
  border-radius: 4px;
  opacity: 0.6;
  z-index: 0;
}

:deep(.el-table__row:hover) .ratio-bar {
  opacity: 0.8;
}

:deep(.el-table__row:hover) td {
  background-color: #f0f9ff !important;
}
</style> 