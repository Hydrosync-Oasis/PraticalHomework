import numpy as np
from .data_loader import load_dataset

def get_age_distribution():
    """获取年龄分布统计数据"""
    df = load_dataset()
    
    if df is None:
        return {"error": "无法加载数据"}
    
    # 年龄分布总体统计
    age_bins = list(range(20, 90, 5))
    age_labels = [f"{start}-{start+4}" for start in age_bins]
    
    # 计算年龄分布直方图
    hist, bin_edges = np.histogram(df['AGE'], bins=age_bins)
    
    # 按照肺癌/非肺癌分组的年龄分布
    cancer_age_data = []
    non_cancer_age_data = []
    
    for i, (start, end) in enumerate(zip(age_bins[:-1], age_bins[1:])):
        cancer_count = df[(df['AGE'] >= start) & (df['AGE'] < end) & (df['LUNG_CANCER'] == 'YES')].shape[0]
        non_cancer_count = df[(df['AGE'] >= start) & (df['AGE'] < end) & (df['LUNG_CANCER'] == 'NO')].shape[0]
        
        cancer_age_data.append(cancer_count)
        non_cancer_age_data.append(non_cancer_count)
    
    # 箱型图数据
    cancer_df = df[df['LUNG_CANCER'] == 'YES']
    non_cancer_df = df[df['LUNG_CANCER'] == 'NO']
    
    boxplot_data = {
        "肺癌": {
            "min": int(cancer_df['AGE'].min()),
            "max": int(cancer_df['AGE'].max()),
            "median": int(cancer_df['AGE'].median()),
            "q1": int(cancer_df['AGE'].quantile(0.25)),
            "q3": int(cancer_df['AGE'].quantile(0.75))
        },
        "非肺癌": {
            "min": int(non_cancer_df['AGE'].min()),
            "max": int(non_cancer_df['AGE'].max()),
            "median": int(non_cancer_df['AGE'].median()),
            "q1": int(non_cancer_df['AGE'].quantile(0.25)),
            "q3": int(non_cancer_df['AGE'].quantile(0.75))
        }
    }
    
    return {
        "histogramData": {
            "labels": age_labels,
            "data": hist.tolist()
        },
        "groupedData": {
            "labels": age_labels,
            "cancer": cancer_age_data,
            "nonCancer": non_cancer_age_data
        },
        "boxplotData": boxplot_data,
        "ageStatistics": {
            "mean": float(df['AGE'].mean()),
            "median": float(df['AGE'].median()),
            "min": int(df['AGE'].min()),
            "max": int(df['AGE'].max()),
        }
    } 