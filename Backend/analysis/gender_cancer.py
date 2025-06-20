from .data_loader import load_dataset

def get_gender_cancer_stats():
    """获取性别与肺癌关系的统计数据"""
    df = load_dataset()
    
    if df is None:
        return {"error": "无法加载数据"}
    
    # 计算性别与肺癌的交叉表
    gender_cancer = df.groupby(['GENDER_LABEL', 'LUNG_CANCER_LABEL']).size().unstack(fill_value=0)
    
    # 将数据转换为ECharts格式
    male_cancer = int(gender_cancer.loc['男', '肺癌'])
    male_non_cancer = int(gender_cancer.loc['男', '非肺癌'])
    female_cancer = int(gender_cancer.loc['女', '肺癌'])
    female_non_cancer = int(gender_cancer.loc['女', '非肺癌'])
    
    # 计算百分比
    male_total = male_cancer + male_non_cancer
    female_total = female_cancer + female_non_cancer
    
    male_cancer_percent = round(male_cancer / male_total * 100, 1) if male_total > 0 else 0
    female_cancer_percent = round(female_cancer / female_total * 100, 1) if female_total > 0 else 0
    
    # 返回数据
    return {
        "barData": {
            "categories": ["男", "女"],
            "series": [
                {
                    "name": "肺癌",
                    "data": [male_cancer, female_cancer]
                },
                {
                    "name": "非肺癌",
                    "data": [male_non_cancer, female_non_cancer]
                }
            ]
        },
        "pieData": [
            {
                "name": "男性",
                "value": [male_cancer, male_non_cancer],
                "percent": male_cancer_percent
            },
            {
                "name": "女性", 
                "value": [female_cancer, female_non_cancer],
                "percent": female_cancer_percent
            }
        ],
        "summary": {
            "totalMale": male_total,
            "totalFemale": female_total,
            "maleCancer": male_cancer,
            "femaleCancer": female_cancer,
            "maleNonCancer": male_non_cancer,
            "femaleNonCancer": female_non_cancer,
        }
    } 