import pandas as pd
import numpy as np
from pathlib import Path

def load_dataset():
    """加载肺癌数据集并进行基本处理"""
    base_dir = Path(__file__).resolve().parent.parent
    data_path = base_dir / 'data' / 'lung_cancer.csv'
    
    try:
        df = pd.read_csv(data_path)
        df.columns = df.columns.str.strip()
        
        # 将LUNG_CANCER转换为数字
        df['LUNG_CANCER_NUMERIC'] = df['LUNG_CANCER'].map({'YES': 1, 'NO': 0})
        
        # 将GENDER转换为数字
        df['GENDER_NUMERIC'] = df['GENDER'].map({'M': 1, 'F': 0})
        
        # 为了更好地处理，同时保留原始分类
        df['GENDER_LABEL'] = df['GENDER'].map({'M': '男', 'F': '女'})
        df['LUNG_CANCER_LABEL'] = df['LUNG_CANCER'].map({'YES': '肺癌', 'NO': '非肺癌'})
        
        return df
    except Exception as e:
        print(f"加载数据时出错: {e}")
        return None 