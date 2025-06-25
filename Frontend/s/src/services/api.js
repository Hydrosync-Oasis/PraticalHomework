import axios from 'axios';

const API_URL = 'http://localhost:5000/api';

// 创建axios实例
const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  }
});

// 数据分析相关API
export const analysisApi = {
  // 获取年龄分布数据
  getAgeDistribution() {
    return apiClient.get('/analysis/age-distribution');
  },
  
  // 获取性别与肺癌关系数据
  getGenderCancer() {
    return apiClient.get('/analysis/gender-cancer');
  },
  
  // 获取特征相关性矩阵
  getCorrelationMatrix() {
    return apiClient.get('/analysis/correlation-matrix');
  },
  
  // 获取年龄组统计数据
  getAgeGroupStats() {
    return apiClient.get('/analysis/age-group-stats');
  },
  
  // 获取吸烟与年龄统计数据
  getSmokingStats() {
    return apiClient.get('/analysis/smoking-stats');
  },
  
  // 获取患者数量统计数据
  getPatientCounts() {
    return apiClient.get('/analysis/patient-counts');
  }
};

// 数据可视化大屏相关API
export const dashboardApi = {
  // 获取箱线图数据（吸烟者与收费关系）
  getBoxplotData() {
    return apiClient.get('/analysis/boxplot');
  },
  
  // 获取BMI与收费散点图数据
  getScatterBmiData() {
    return apiClient.get('/analysis/scatter_bmi');
  },
  
  // 获取年龄直方图数据
  getAgeHistData() {
    return apiClient.get('/analysis/age_hist');
  },
  
  // 获取地区平均收费数据
  getRegionAvgData() {
    return apiClient.get('/analysis/region_avg');
  },
  
  // 获取年龄与收费及吸烟者散点图数据
  getScatterAgeData() {
    return apiClient.get('/analysis/scatter_age');
  },
  
  // 获取相关性数据
  getCorrelationData() {
    return apiClient.get('/analysis/correlation');
  }
};

export default { analysisApi, dashboardApi }; 