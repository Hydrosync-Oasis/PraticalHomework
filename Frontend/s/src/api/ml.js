// 机器学习相关接口
import axios from './index'

export function PredictLungCancer(data) {
    return axios.post('/predict', data)
}

export function PredictDiabetes(data) {
    return axios.post('/predict_diabetes', data)
}

export function PredictTumor(data) {
    return axios.post('/predict/brain_tumor', data)
}

export function PredictTumorPosition(data) {
    return axios.post('/yolo_detect', data, {
        responseType: 'blob'
    })
}