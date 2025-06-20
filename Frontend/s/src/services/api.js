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

// 预测相关API
export const predictionApi = {
  // 提交用户数据进行预测
  predictCancer(userData) {
    return apiClient.post('/predict', userData);
  }
};

export default { analysisApi, predictionApi }; 