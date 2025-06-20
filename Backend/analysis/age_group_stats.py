import pandas as pd
from .data_loader import load_dataset

def get_age_group_stats():
    """获取不同年龄组的肺癌与非肺癌患者统计"""
    df = load_dataset()
    
    if df is None:
        return {"error": "无法加载数据"}
    
    # 定义年龄组区间
    age_bins = [20, 30, 40, 50, 60, 70, 80, 90]
    age_labels = ['20-29岁', '30-39岁', '40-49岁', '50-59岁', '60-69岁', '70-79岁', '80+岁']
    
    # 添加年龄组分类
    df['age_group'] = pd.cut(df['AGE'], bins=age_bins, labels=age_labels, right=False)
    
    # 按年龄组和肺癌状态统计
    grouped = df.groupby(['age_group', 'LUNG_CANCER_LABEL']).size().unstack(fill_value=0)
    
    # 确保所有列都存在
    if '肺癌' not in grouped.columns:
        grouped['肺癌'] = 0
    if '非肺癌' not in grouped.columns:
        grouped['非肺癌'] = 0
    
    # 计算每个年龄组的总人数和肺癌比例
    grouped['总数'] = grouped['肺癌'] + grouped['非肺癌']
    grouped['肺癌比例'] = grouped['肺癌'] / grouped['总数']
    
    # 重新索引以确保所有年龄组都有数据
    all_groups = pd.DataFrame(index=age_labels)
    grouped = grouped.reindex(all_groups.index).fillna(0)
    
    # 构造ECharts格式的数据
    categories = age_labels
    cancer_data = grouped['肺癌'].astype(int).tolist()
    non_cancer_data = grouped['非肺癌'].astype(int).tolist()
    ratio_data = [round(ratio * 100, 1) for ratio in grouped['肺癌比例'].tolist()]
    
    # 数据汇总
    age_summary = []
    for age, cancer, non_cancer, ratio in zip(categories, cancer_data, non_cancer_data, ratio_data):
        age_summary.append({
            "ageGroup": age,
            "cancer": int(cancer),
            "nonCancer": int(non_cancer),
            "total": int(cancer + non_cancer),
            "ratio": float(ratio)
        })
    
    # 按总数排序
    age_summary = sorted(age_summary, key=lambda x: x["total"], reverse=True)
    
    return {
        "stackBarData": {
            "categories": categories,
            "cancer": cancer_data,
            "nonCancer": non_cancer_data
        },
        "lineData": {
            "categories": categories,
            "ratios": ratio_data
        },
        "summary": age_summary
    } 