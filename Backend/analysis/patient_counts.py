from .data_loader import load_dataset

def get_patient_counts():
    """获取肺癌与非肺癌患者数量统计"""
    df = load_dataset()
    
    if df is None:
        return {"error": "无法加载数据"}
    
    # 患者总数统计
    cancer_count = df[df['LUNG_CANCER'] == 'YES'].shape[0]
    non_cancer_count = df[df['LUNG_CANCER'] == 'NO'].shape[0]
    total_count = cancer_count + non_cancer_count
    
    # 计算比例
    cancer_percent = round(cancer_count / total_count * 100, 1)
    non_cancer_percent = round(non_cancer_count / total_count * 100, 1)
    
    # 按性别统计肺癌和非肺癌患者
    male_cancer = df[(df['GENDER'] == 'M') & (df['LUNG_CANCER'] == 'YES')].shape[0]
    male_non_cancer = df[(df['GENDER'] == 'M') & (df['LUNG_CANCER'] == 'NO')].shape[0]
    female_cancer = df[(df['GENDER'] == 'F') & (df['LUNG_CANCER'] == 'YES')].shape[0]
    female_non_cancer = df[(df['GENDER'] == 'F') & (df['LUNG_CANCER'] == 'NO')].shape[0]
    
    # 计算各组比例
    male_total = male_cancer + male_non_cancer
    female_total = female_cancer + female_non_cancer
    
    male_cancer_percent = round(male_cancer / male_total * 100, 1) if male_total > 0 else 0
    female_cancer_percent = round(female_cancer / female_total * 100, 1) if female_total > 0 else 0
    
    # 按肺癌危险因素统计患者数量
    risk_factors = [
        'SMOKING', 'YELLOW_FINGERS', 'ANXIETY', 'PEER_PRESSURE',
        'CHRONIC DISEASE', 'FATIGUE', 'ALLERGY', 'WHEEZING',
        'ALCOHOL CONSUMING', 'COUGHING', 'SHORTNESS OF BREATH',
        'SWALLOWING DIFFICULTY', 'CHEST PAIN'
    ]
    
    # 构建中文标签映射
    factor_labels = {
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
        'CHEST PAIN': '胸痛'
    }
    
    # 统计各危险因素的患者数量
    risk_factor_stats = []
    for factor in risk_factors:
        # 值为2表示存在此风险因素
        has_factor_cancer = df[(df[factor] == 2) & (df['LUNG_CANCER'] == 'YES')].shape[0]
        has_factor_non_cancer = df[(df[factor] == 2) & (df['LUNG_CANCER'] == 'NO')].shape[0]
        no_factor_cancer = df[(df[factor] == 1) & (df['LUNG_CANCER'] == 'YES')].shape[0]
        no_factor_non_cancer = df[(df[factor] == 1) & (df['LUNG_CANCER'] == 'NO')].shape[0]
        
        has_factor_total = has_factor_cancer + has_factor_non_cancer
        no_factor_total = no_factor_cancer + no_factor_non_cancer
        
        has_factor_cancer_percent = round(has_factor_cancer / has_factor_total * 100, 1) if has_factor_total > 0 else 0
        no_factor_cancer_percent = round(no_factor_cancer / no_factor_total * 100, 1) if no_factor_total > 0 else 0
        
        risk_factor_stats.append({
            "factor": factor_labels[factor],
            "hasFactor": {
                "cancer": has_factor_cancer,
                "nonCancer": has_factor_non_cancer,
                "total": has_factor_total,
                "cancerPercent": has_factor_cancer_percent
            },
            "noFactor": {
                "cancer": no_factor_cancer,
                "nonCancer": no_factor_non_cancer,
                "total": no_factor_total,
                "cancerPercent": no_factor_cancer_percent
            },
            "cancerRatio": round(has_factor_cancer_percent / no_factor_cancer_percent, 2) if no_factor_cancer_percent > 0 else 0
        })
    
    # 按肺癌比例排序风险因素
    risk_factor_stats = sorted(risk_factor_stats, key=lambda x: x["cancerRatio"], reverse=True)
    
    # 提取排序后的风险因素名称和肺癌比例，用于生成条形图
    factor_names = [item["factor"] for item in risk_factor_stats]
    factor_ratios = [item["cancerRatio"] for item in risk_factor_stats]
    
    return {
        "overallStats": {
            "cancer": cancer_count,
            "nonCancer": non_cancer_count,
            "total": total_count,
            "cancerPercent": cancer_percent,
            "nonCancerPercent": non_cancer_percent
        },
        "genderStats": {
            "male": {
                "cancer": male_cancer,
                "nonCancer": male_non_cancer,
                "total": male_total,
                "cancerPercent": male_cancer_percent
            },
            "female": {
                "cancer": female_cancer,
                "nonCancer": female_non_cancer,
                "total": female_total,
                "cancerPercent": female_cancer_percent
            }
        },
        "riskFactors": {
            "factors": factor_names,
            "ratios": factor_ratios,
            "details": risk_factor_stats
        }
    } 