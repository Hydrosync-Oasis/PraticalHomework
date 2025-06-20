import numpy as np
from .data_loader import load_dataset

def get_correlation_matrix():
    """获取特征相关性矩阵数据"""
    df = load_dataset()
    
    if df is None:
        return {"error": "无法加载数据"}
    
    # 转换分类特征为数字以计算相关性
    numeric_columns = ['AGE', 'GENDER_NUMERIC', 'SMOKING', 'YELLOW_FINGERS', 
                      'ANXIETY', 'PEER_PRESSURE', 'CHRONIC DISEASE', 
                      'FATIGUE', 'ALLERGY', 'WHEEZING', 'ALCOHOL CONSUMING',
                      'COUGHING', 'SHORTNESS OF BREATH', 'SWALLOWING DIFFICULTY',
                      'CHEST PAIN', 'LUNG_CANCER_NUMERIC']
    
    # 计算相关性矩阵
    corr_matrix = df[numeric_columns].corr()
    
    # 美化特征名称
    feature_names = {
        'AGE': '年龄',
        'GENDER_NUMERIC': '性别',
        'SMOKING': '吸烟',
        'YELLOW_FINGERS': '黄手指',
        'ANXIETY': '焦虑',
        'PEER_PRESSURE': '同伴压力',
        'CHRONIC DISEASE': '慢性疾病',
        'FATIGUE': '疲劳',
        'ALLERGY': '过敏',
        'WHEEZING': '喘息',
        'ALCOHOL CONSUMING': '饮酒',
        'COUGHING': '咳嗽',
        'SHORTNESS OF BREATH': '呼吸困难',
        'SWALLOWING DIFFICULTY': '吞咽困难',
        'CHEST PAIN': '胸痛',
        'LUNG_CANCER_NUMERIC': '肺癌'
    }
    
    # 构造ECharts格式的数据
    categories = [feature_names[col] for col in numeric_columns]
    
    data = []
    for i, row in enumerate(numeric_columns):
        for j, col in enumerate(numeric_columns):
            # 只需要下三角矩阵的数据
            if i >= j:
                data.append([j, i, round(corr_matrix.loc[row, col], 2)])
    
    # 返回相关性最高的特征对
    corr_without_diagonal = corr_matrix.copy()
    np.fill_diagonal(corr_without_diagonal.values, 0)  # 去除对角线的自相关
    
    # 获取相关性最高的特征对
    high_corr = []
    for i, row in enumerate(numeric_columns):
        for j, col in enumerate(numeric_columns):
            if i > j:  # 只取下三角
                corr_value = corr_matrix.loc[row, col]
                if abs(corr_value) >= 0.5:  # 只关注相关性较高的特征
                    high_corr.append({
                        "feature1": feature_names[row],
                        "feature2": feature_names[col],
                        "correlation": round(corr_value, 2)
                    })
    
    # 按相关性绝对值从高到低排序
    high_corr = sorted(high_corr, key=lambda x: abs(x["correlation"]), reverse=True)
    
    return {
        "correlationMatrix": {
            "categories": categories,
            "data": data
        },
        "highCorrelation": high_corr[:10]  # 返回相关性最高的10个特征对
    } 