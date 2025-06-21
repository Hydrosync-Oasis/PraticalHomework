// 机器学习相关接口
import axios from './index'

export function PredictLungCancer(data) {
    return axios.post('/predict', data)
}

export function PredictDiabetes(data) {
    return axios.post('/predict_diabetes', data)
}

