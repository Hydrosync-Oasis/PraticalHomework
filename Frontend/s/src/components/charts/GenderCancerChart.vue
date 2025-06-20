<template>
  <div class="gender-cancer-charts">
    <el-alert
      v-if="showAll && error"
      title="数据加载错误"
      type="error"
      description="性别分布数据加载失败，请稍后重试"
      show-icon
      :closable="false"
      style="margin-bottom: 20px;"
    />

    <chart-wrapper 
      v-if="showAll && pieChartOption && Object.keys(pieChartOption).length > 0"
      title="性别与肺癌患病率" 
      subtitle="不同性别的肺癌患病率对比"
      intro="该环形图展示了男性和女性人群中患有肺癌的比例。从图表可以看出，男性和女性的肺癌患病率存在一定差异，有助于分析性别因素对肺癌发病的影响。"
      :option="pieChartOption" 
      :loading="loading"
      :error="false"
      height="400px">
      <template #data-table>
        <div class="data-summary" v-if="chartData && chartData.pieData">
          <h4>性别肺癌患病率统计</h4>
          <el-table :data="genderRatioData" stripe style="width: 100%" :border="true" size="small">
            <el-table-column prop="gender" label="性别" width="180" />
            <el-table-column prop="cancer" label="肺癌人数" width="120" />
            <el-table-column prop="nonCancer" label="非肺癌人数" width="120" />
            <el-table-column prop="total" label="总人数" width="120" />
            <el-table-column prop="ratio" label="肺癌比例">
              <template #default="scope">
                <div class="ratio-cell">
                  <span>{{ scope.row.ratio }}%</span>
                  <div class="ratio-bar" :style="{width: scope.row.ratio + '%', backgroundColor: scope.row.gender === '男性' ? '#1890ff' : '#ff6b81'}"></div>
                </div>
              </template>
            </el-table-column>
          </el-table>
        </div>
      </template>
    </chart-wrapper>
      
    <chart-wrapper 
      v-if="showAll && barChartOption && Object.keys(barChartOption).length > 0"
      title="性别分组柱状图" 
      subtitle="按性别划分的肺癌患者与非肺癌患者数量"
      intro="该柱状图对比了男性和女性中肺癌患者和非肺癌患者的分布情况。通过对比不同性别人群中的肺癌患病情况，可以直观地看出性别与肺癌之间的关系。"
      :option="barChartOption" 
      :loading="loading"
      :error="false"
      height="400px">
      <template #data-table>
        <div class="data-summary" v-if="chartData && chartData.summary">
          <h4>性别与肺癌关系统计摘要</h4>
          <el-descriptions :column="3" border size="small">
            <el-descriptions-item label="总样本数">{{ chartData.summary.totalMale + chartData.summary.totalFemale }} 人</el-descriptions-item>
            <el-descriptions-item label="男性总数">{{ chartData.summary.totalMale }} 人</el-descriptions-item>
            <el-descriptions-item label="女性总数">{{ chartData.summary.totalFemale }} 人</el-descriptions-item>
            <el-descriptions-item label="肺癌患者总数">{{ chartData.summary.maleCancer + chartData.summary.femaleCancer }} 人</el-descriptions-item>
            <el-descriptions-item label="男性肺癌患者">{{ chartData.summary.maleCancer }} 人</el-descriptions-item>
            <el-descriptions-item label="女性肺癌患者">{{ chartData.summary.femaleCancer }} 人</el-descriptions-item>
            <el-descriptions-item label="非肺癌患者总数">{{ chartData.summary.maleNonCancer + chartData.summary.femaleNonCancer }} 人</el-descriptions-item>
            <el-descriptions-item label="男性非肺癌患者">{{ chartData.summary.maleNonCancer }} 人</el-descriptions-item>
            <el-descriptions-item label="女性非肺癌患者">{{ chartData.summary.femaleNonCancer }} 人</el-descriptions-item>
          </el-descriptions>
        </div>
      </template>
    </chart-wrapper>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import ChartWrapper from '../ChartWrapper.vue'
import { analysisApi } from '@/services/api'

// 状态
const chartData = ref(null)
const loading = ref(false)
const error = ref(false)
const showAll = ref(false)

// 性别比例数据
const genderRatioData = computed(() => {
  if (!chartData.value || !chartData.value.pieData) return []
  
  return chartData.value.pieData.map(item => {
    const cancer = item.value[0]
    const nonCancer = item.value[1]
    const total = cancer + nonCancer
    const ratio = ((cancer / total) * 100).toFixed(1)
    
    return {
      gender: item.name,
      cancer: cancer,
      nonCancer: nonCancer,
      total: total,
      ratio: ratio
    }
  })
})

// 饼图配置
const pieChartOption = computed(() => {
  try {
    if (!chartData.value || !chartData.value.pieData) return {}
    
    const maleData = chartData.value.pieData.find(d => d.name === '男性');
    const femaleData = chartData.value.pieData.find(d => d.name === '女性');
    
    if (!maleData || !femaleData) return {};
    
    const malePercent = maleData.percent || (maleData.value[0] * 100 / (maleData.value[0] + maleData.value[1])).toFixed(1);
    const femalePercent = femaleData.percent || (femaleData.value[0] * 100 / (femaleData.value[0] + femaleData.value[1])).toFixed(1);
    
    return {
      title: {
        text: '不同性别肺癌患病率',
        left: 'center',
        top: 0,
        textStyle: {
          fontSize: 16
        }
      },
      tooltip: {
        trigger: 'item',
        formatter: '{b}: {c}%',
        backgroundColor: 'rgba(255,255,255,0.9)',
        borderColor: '#eeeeee',
        borderWidth: 1,
        textStyle: {
          color: '#333'
        },
        extraCssText: 'box-shadow: 0 0 8px rgba(0, 0, 0, 0.1);'
      },
      legend: {
        orient: 'horizontal',
        bottom: 10,
        left: 'center',
        data: ['男性肺癌率', '女性肺癌率'],
        textStyle: {
          color: '#666'
        },
        icon: 'circle'
      },
      series: [
        {
          name: '肺癌患病率',
          type: 'pie',
          radius: ['40%', '70%'],
          center: ['50%', '50%'],
          avoidLabelOverlap: false,
          itemStyle: {
            borderRadius: 10,
            borderColor: '#fff',
            borderWidth: 2
          },
          label: {
            show: true,
            position: 'outside',
            formatter: '{b}: {c}%',
            color: '#606266',
            fontSize: 14
          },
          emphasis: {
            label: {
              show: true,
              fontSize: 16,
              fontWeight: 'bold'
            },
            itemStyle: {
              shadowBlur: 10,
              shadowOffsetX: 0,
              shadowColor: 'rgba(0, 0, 0, 0.5)'
            }
          },
          labelLine: {
            show: true,
            length: 15,
            length2: 10
          },
          data: [
            { value: malePercent, name: '男性肺癌率', itemStyle: {color: '#1890ff'} },
            { value: femalePercent, name: '女性肺癌率', itemStyle: {color: '#ff6b81'} }
          ]
        }
      ]
    }
  } catch (err) {
    console.error('创建饼图配置出错:', err)
    return {}
  }
})

// 柱状图配置
const barChartOption = computed(() => {
  try {
    if (!chartData.value || !chartData.value.barData) return {}

    const { categories, series } = chartData.value.barData;
    
    return {
      title: {
        text: '性别与肺癌患病情况',
        left: 'center',
        top: 0,
        textStyle: {
          fontSize: 16
        }
      },
      tooltip: {
        trigger: 'axis',
        axisPointer: {
          type: 'shadow'
        },
        formatter: function(params) {
          const category = params[0].axisValue;
          const cancer = params[0].data;
          const nonCancer = params[1].data;
          const total = cancer + nonCancer;
          const ratio = (cancer / total * 100).toFixed(1);
          return `${category}<br/>
                 肺癌患者: ${cancer} 人 (${ratio}%)<br/>
                 非肺癌患者: ${nonCancer} 人<br/>
                 总计: ${total} 人`;
        }
      },
      legend: {
        data: series.map(s => s.name),
        top: 30,
        left: 'center'
      },
      grid: {
        left: '3%',
        right: '4%',
        bottom: '10%',
        top: '80px',
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
          name: '人数'
        }
      ],
      series: series.map((s, index) => ({
        name: s.name,
        type: 'bar',
        stack: '总量',
        emphasis: {
          focus: 'series'
        },
        barWidth: '60%',
        label: {
          show: true,
          position: 'inside',
          formatter: '{c}人',
          color: '#fff'
        },
        data: s.data,
        itemStyle: {
          color: index === 0 ? '#e74c3c' : '#2ecc71'
        }
      }))
    }
  } catch (err) {
    console.error('创建柱状图配置出错:', err)
    return {}
  }
})

// 获取数据
const fetchData = async () => {
  loading.value = true
  error.value = false
  
  try {
    const response = await analysisApi.getGenderCancer()
    chartData.value = response.data
    console.log('性别数据:', chartData.value)
    // 延迟一点显示，等页面稳定后再渲染
    setTimeout(() => {
      showAll.value = true
    }, 200)
  } catch (err) {
    console.error('获取性别与肺癌关系数据失败:', err)
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
.gender-cancer-charts {
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
}

:deep(.el-table td) {
  padding: 12px 0;
}

:deep(.el-table--striped .el-table__body tr.el-table__row--striped td) {
  background-color: #fafafa;
}

:deep(.el-descriptions) {
  padding: 15px;
  background: #f5f7fa;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

:deep(.el-descriptions__title) {
  color: #303133;
  font-weight: 600;
  font-size: 16px;
}

:deep(.el-descriptions__label) {
  color: #606266;
  font-weight: 500;
}

:deep(.el-descriptions__content) {
  color: #303133;
  font-weight: 500;
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
</style> 