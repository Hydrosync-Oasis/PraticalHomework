# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')  # Python 3.7+
import pandas as pd
import numpy as np
import warnings
import seaborn as sns
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import RandomOverSampler
from sklearn.svm import SVC
from sklearn.model_selection import RandomizedSearchCV
from sklearn.metrics import confusion_matrix, classification_report, roc_curve, auc
import joblib
import matplotlib.pyplot as plt

from utils.visualize import (
    plot_age_distribution,
    plot_categorical_counts,
    plot_correlation_heatmap,
    plot_gender_cancer_counts,
    plot_age_group_stacked_bar,
    plot_smoking_boxplot,
    plot_sample_counts_before_after_sampling
)

warnings.filterwarnings('ignore')

from pathlib import Path

def main():
    base_dir = Path(__file__).resolve().parent
    models_dir = base_dir / 'models'

    try:
        base_dir = Path(__file__).resolve().parent
        data_path = base_dir / 'data' / 'lung_cancer.csv'
        df = pd.read_csv(data_path)
    except FileNotFoundError:
        print("错误：未找到数据文件 lung_cancer.csv，请确认文件路径是否正确。")
        return


    print("数据预览：")
    print(df.head())

    print(f"肺癌患者（LUNG_CANCER=NO）数量: {df[df['LUNG_CANCER'] == 'NO'].shape[0]}")
    print(f"数据总行数: {df.shape[0]}")
    df.info()
    print(df.describe())

    print(f"重复数据条数: {df.duplicated().sum()}")
    df.drop_duplicates(inplace=True)
    print(f"去重后数据条数: {df.shape[0]}")

    encoder = LabelEncoder()
    df['LUNG_CANCER'] = encoder.fit_transform(df['LUNG_CANCER'])
    df['GENDER'] = encoder.fit_transform(df['GENDER'])

    df.columns = df.columns.str.strip()

    cat_col = [
        'GENDER', 'SMOKING', 'YELLOW_FINGERS', 'ANXIETY', 'PEER_PRESSURE',
        'CHRONIC DISEASE', 'FATIGUE', 'ALLERGY', 'WHEEZING',
        'ALCOHOL CONSUMING', 'COUGHING', 'SHORTNESS OF BREATH',
        'SWALLOWING DIFFICULTY', 'CHEST PAIN'
    ]

    # 反编码LUNG_CANCER用于绘图（字符串类别）
    df_plot = df.copy()
    df_plot['LUNG_CANCER'] = df_plot['LUNG_CANCER'].map({0: 'NO', 1: 'YES'})

    # 画图，按需要选择传入df或df_plot
    plot_age_distribution(df_plot)
    plot_categorical_counts(df_plot, cat_col)
    plot_correlation_heatmap(df)              # 这里用纯数值df
    plot_gender_cancer_counts(df_plot)
    plot_age_group_stacked_bar(df_plot)
    plot_smoking_boxplot(df_plot)
    plot_sample_counts_before_after_sampling(df)

    X = df.drop(['LUNG_CANCER'], axis=1).copy()
    y = df['LUNG_CANCER']

    for col in X.columns[2:]:
        X.loc[:, col] = X[col] - 1

    ros = RandomOverSampler(random_state=42)
    X_resampled, y_resampled = ros.fit_resample(X, y)

    X_train, X_test, y_train, y_test = train_test_split(
        X_resampled, y_resampled, test_size=0.25, random_state=42, stratify=y_resampled)

    print(f"训练集大小: {X_train.shape}")
    print(f"测试集大小: {X_test.shape}")

    scaler = StandardScaler()
    X_train.loc[:, 'AGE'] = scaler.fit_transform(X_train[['AGE']])
    X_test.loc[:, 'AGE'] = scaler.transform(X_test[['AGE']])

    joblib.dump(scaler, 'models/scaler.pkl')

    param_grid = {
        'C': [0.001, 0.01, 0.1, 1, 10, 100],
        'gamma': [0.001, 0.01, 0.1, 1, 10, 100]
    }
    svc = SVC(probability=True, random_state=42)
    rcv = RandomizedSearchCV(svc, param_grid, cv=5, random_state=42)
    rcv.fit(X_train, y_train)

    print(f"最佳参数: {rcv.best_params_}")

    y_pred = rcv.predict(X_test)
    cm = confusion_matrix(y_test, y_pred)
    print("混淆矩阵：")
    print(cm)
    print("分类报告：")
    print(classification_report(y_test, y_pred))

    plt.figure(figsize=(6, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Oranges')
    plt.title('混淆矩阵')
    plt.xlabel('预测值')
    plt.ylabel('真实值')
    plt.show()

    y_prob = rcv.predict_proba(X_test)[:, 1]
    fpr, tpr, _ = roc_curve(y_test, y_prob)
    roc_auc = auc(fpr, tpr)

    plt.figure(figsize=(6, 6))
    plt.plot(fpr, tpr, color='red', lw=2, label=f'ROC曲线 (AUC = {roc_auc:.2f})')
    plt.plot([0, 1], [0, 1], color='gray', linestyle='--')
    plt.title('ROC曲线')
    plt.xlabel('假阳性率')
    plt.ylabel('真阳性率')
    plt.legend(loc='lower right')
    plt.show()

    joblib.dump(rcv.best_estimator_, 'models/best_lung_cancer_model.pkl')
    print("模型已保存至 best_lung_cancer_model.pkl")

    sample_data = pd.DataFrame({
        'GENDER': ['F'],
        'AGE': [60],
        'SMOKING': [1],
        'YELLOW_FINGERS': [1],
        'ANXIETY': [1],
        'PEER_PRESSURE': [1],
        'CHRONIC DISEASE': [1],
        'FATIGUE': [1],
        'ALLERGY': [1],
        'WHEEZING': [1],
        'ALCOHOL CONSUMING': [1],
        'COUGHING': [1],
        'SHORTNESS OF BREATH': [1],
        'SWALLOWING DIFFICULTY': [1],
        'CHEST PAIN': [1]
    }).copy()

    sample_data.loc[:, 'AGE'] = scaler.transform(sample_data[['AGE']])
    for col in sample_data.columns[2:]:
        sample_data.loc[:, col] = sample_data[col] - 1
    sample_data.loc[:, 'GENDER'] = sample_data['GENDER'].replace({'M': 1, 'F': 0})

    loaded_model = joblib.load('models/best_lung_cancer_model.pkl')
    sample_pred = loaded_model.predict(sample_data)
    sample_proba = loaded_model.predict_proba(sample_data)[:, 1]
    print(f"示例预测结果: {'肺癌' if sample_pred[0] == 1 else '非肺癌'}")
    print(f"示例预测概率: {sample_proba[0]:.4f}")
    print("示例数据（预处理后）：")
    print(sample_data)

if __name__ == "__main__":
    main()
