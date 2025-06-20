import numpy as np
from .data_loader import load_dataset

def get_smoking_stats():
    """获取吸烟与肺癌的统计数据"""
    df = load_dataset()
    
    if df is None:
        return {"error": "无法加载数据"}
    
    # 吸烟者与非吸烟者的年龄箱线图数据
    smoking_df = df[df['SMOKING'] == 2]  # 2表示吸烟
    non_smoking_df = df[df['SMOKING'] == 1]  # 1表示不吸烟
    
    # 箱型图数据
    boxplot_data = {
        "吸烟": {
            "min": int(smoking_df['AGE'].min()),
            "max": int(smoking_df['AGE'].max()),
            "median": int(smoking_df['AGE'].median()),
            "q1": int(smoking_df['AGE'].quantile(0.25)),
            "q3": int(smoking_df['AGE'].quantile(0.75))
        },
        "不吸烟": {
            "min": int(non_smoking_df['AGE'].min()),
            "max": int(non_smoking_df['AGE'].max()),
            "median": int(non_smoking_df['AGE'].median()),
            "q1": int(non_smoking_df['AGE'].quantile(0.25)),
            "q3": int(non_smoking_df['AGE'].quantile(0.75))
        }
    }
    
    # 吸烟状态与肺癌的关系
    smoking_cancer = smoking_df[smoking_df['LUNG_CANCER'] == 'YES'].shape[0]
    smoking_non_cancer = smoking_df[smoking_df['LUNG_CANCER'] == 'NO'].shape[0]
    non_smoking_cancer = non_smoking_df[non_smoking_df['LUNG_CANCER'] == 'YES'].shape[0]
    non_smoking_non_cancer = non_smoking_df[non_smoking_df['LUNG_CANCER'] == 'NO'].shape[0]
    
    # 计算比例
    smoking_total = smoking_cancer + smoking_non_cancer
    non_smoking_total = non_smoking_cancer + non_smoking_non_cancer
    
    smoking_cancer_ratio = round(smoking_cancer / smoking_total * 100, 1) if smoking_total > 0 else 0
    non_smoking_cancer_ratio = round(non_smoking_cancer / non_smoking_total * 100, 1) if non_smoking_total > 0 else 0
    
    # 年龄分组
    age_bins = [20, 30, 40, 50, 60, 70, 80, 90]
    age_labels = ['20-29岁', '30-39岁', '40-49岁', '50-59岁', '60-69岁', '70-79岁', '80+岁']
    
    smoking_by_age = []
    for i, (start, end) in enumerate(zip(age_bins[:-1], age_bins[1:])):
        age_group = age_labels[i]
        age_range_df = df[(df['AGE'] >= start) & (df['AGE'] < end)]
        
        smoking_count = age_range_df[age_range_df['SMOKING'] == 2].shape[0]
        non_smoking_count = age_range_df[age_range_df['SMOKING'] == 1].shape[0]
        
        total_in_age = smoking_count + non_smoking_count
        smoking_percent = round(smoking_count / total_in_age * 100, 1) if total_in_age > 0 else 0
        
        smoking_by_age.append({
            "ageGroup": age_group,
            "smoking": smoking_count,
            "nonSmoking": non_smoking_count,
            "total": total_in_age,
            "smokingPercent": smoking_percent
        })
    
    return {
        "boxplotData": boxplot_data,
        "smokingCancerData": {
            "categories": ["吸烟", "不吸烟"],
            "cancer": [smoking_cancer, non_smoking_cancer],
            "nonCancer": [smoking_non_cancer, non_smoking_non_cancer],
            "cancerRatio": [smoking_cancer_ratio, non_smoking_cancer_ratio]
        },
        "smokingByAge": smoking_by_age,
        "summary": {
            "totalSmoking": smoking_total,
            "totalNonSmoking": non_smoking_total,
            "smokingCancer": smoking_cancer,
            "nonSmokingCancer": non_smoking_cancer
        }
    } 