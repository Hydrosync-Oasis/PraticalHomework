import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix, classification_report, roc_curve, roc_auc_score
from imblearn.over_sampling import RandomOverSampler
import joblib
from pathlib import Path
import warnings
# 设置中文字体（SimHei 是常见中文黑体）
plt.rcParams['font.family'] = 'SimHei'

# 正常显示负号
plt.rcParams['axes.unicode_minus'] = False
def main():
    warnings.filterwarnings('ignore')
    plt.style.use('fivethirtyeight')
    colors = ['#011f4b', '#03396c', '#005b96', '#6497b1', '#b3cde0']
    sns.set_palette(sns.color_palette(colors))

    # 0) 路径设置
    base_dir = Path(__file__).resolve().parent
    data_path = base_dir / 'data' / 'lung_cancer.csv'
    models_dir = base_dir / 'models'
    models_dir.mkdir(exist_ok=True)

    # 1) 读取数据
    try:
        df = pd.read_csv(data_path)
    except FileNotFoundError:
        print("❌ 错误：未找到数据文件 lung_cancer.csv，请确认 data 目录存在且文件在其中。")
        return

    # 2) 数据描述
    print("非肺癌样本数量：", df[df['LUNG_CANCER'] == 'NO'].shape[0])
    print("数据总维度：", df.shape)
    df.info()
    print(df.describe())

    explore = df.describe().T
    explore['R'] = explore['max'] - explore['min']
    explore['IQR'] = explore['75%'] - explore['25%']
    explore['cv'] = explore['std'] / explore['mean']
    explore['std2'] = explore['std'] ** 2
    explore['median'] = np.median(df.iloc[:, 1])
    explore['mode'] = np.argmax(np.bincount(df.iloc[:, 1]))
    print(explore)

    # 3) 缺失值与重复值
    print(df.isnull().sum())
    print(df.duplicated().sum())
    df.drop_duplicates(inplace=True)

    # 4) 标签编码
    encoder = LabelEncoder()
    df['LUNG_CANCER'] = encoder.fit_transform(df['LUNG_CANCER'])
    df['GENDER'] = encoder.fit_transform(df['GENDER'])

    # 5) 分类变量列名
    cat_col = [col for col in df.columns if col not in ['AGE', 'LUNG_CANCER']]

    # 6) 可视化
    fig, ax = plt.subplots(1, 3, figsize=(20, 6))
    sns.histplot(df['AGE'], ax=ax[0], kde=True)
    sns.histplot(data=df, x='AGE', hue='LUNG_CANCER', ax=ax[1], kde=True)
    sns.boxplot(x='LUNG_CANCER', y='AGE', data=df, ax=ax[2])
    plt.suptitle("Visualizing AGE column", size=20)
    plt.show()

    fig, ax = plt.subplots(len(cat_col), 2, figsize=(30, len(cat_col)*3))
    for i, col in enumerate(cat_col):
        sns.countplot(data=df, x=col, ax=ax[i, 0])
        sns.countplot(data=df, x=col, hue='LUNG_CANCER', ax=ax[i, 1])
    fig.tight_layout()
    fig.subplots_adjust(top=0.95)
    plt.suptitle("Visualizing Categorical Columns", fontsize=30)
    plt.show()

    # 7) 相关性热力图
    corr_matrix = df.corr()
    mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, fmt=".2f", mask=mask, cmap='coolwarm',
                cbar_kws={'shrink': 0.3}, annot_kws={'size': 8})
    plt.title("Feature Correlation Heatmap", fontsize=20)
    plt.show()

    target_corr = corr_matrix['LUNG_CANCER'].abs().sort_values(ascending=False)
    print("\n相关性较强的特征：\n", target_corr[target_corr > 0.1])

    # 8) 特征处理
    X = df.drop('LUNG_CANCER', axis=1)
    y = df['LUNG_CANCER']
    for col in X.columns:
        if col not in ['GENDER', 'AGE']:
            X[col] = X[col] - 1

    # 9) 过采样
    X_over, y_over = RandomOverSampler(random_state=42).fit_resample(X, y)

    # 10) 数据集划分
    X_train, X_test, y_train, y_test = train_test_split(X_over, y_over, test_size=0.2, random_state=42, stratify=y_over)

    # 11) 分布图
    plt.figure(figsize=(15, 15))
    for i, feature in enumerate(X_train.columns, 1):
        plt.subplot(len(X_train.columns)//3+1, 3, i)
        sns.kdeplot(X_train[feature], color='blue', label='Train')
        sns.kdeplot(X_test[feature], color='red', label='Test')
        plt.title(f'Distribution of {feature}')
    plt.legend()
    plt.tight_layout()
    plt.show()

    # 12) 标准化
    scaler = StandardScaler()
    X_train['AGE'] = scaler.fit_transform(X_train[['AGE']])
    X_test['AGE'] = scaler.transform(X_test[['AGE']])

    # 13) 模型训练
    param_grid = {
        'C': [0.001, 0.01, 0.1, 1, 10, 100],
        'gamma': [0.001, 0.01, 0.1, 1, 10, 100]
    }
    svc = SVC(probability=True, random_state=42)
    rcv = RandomizedSearchCV(svc, param_grid, n_iter=10, cv=5, random_state=42)
    rcv.fit(X_train, y_train)

    # 14) 评估
    y_pred = rcv.predict(X_test)
    print("最佳参数:", rcv.best_params_)
    print(classification_report(y_test, y_pred))
    sns.heatmap(confusion_matrix(y_test, y_pred), annot=True, fmt='d', cmap='Blues')
    plt.title("混淆矩阵")
    plt.xlabel("预测值")
    plt.ylabel("真实值")
    plt.show()

    # 15) ROC曲线
    y_proba = rcv.predict_proba(X_test)[:, 1]
    fpr, tpr, _ = roc_curve(y_test, y_proba)
    auc = roc_auc_score(y_test, y_proba)
    plt.figure(figsize=(6, 6))
    plt.plot(fpr, tpr, label=f"AUC = {auc:.3f}")
    plt.plot([0, 1], [0, 1], 'k--')
    plt.xlabel("假阳性率")
    plt.ylabel("真阳性率")
    plt.title("ROC Curve")
    plt.legend()
    plt.show()

    # 16) 保存模型和Scaler
    joblib.dump(rcv.best_estimator_, models_dir / 'best_lung_cancer_model.pkl')
    joblib.dump(scaler, models_dir / 'scaler.pkl')
    print("✅ 模型和标准化器已保存到 models/ 目录。")
    print("训练时特征列名:", X.columns.tolist())


if __name__ == "__main__":
    main()
