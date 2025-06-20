import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import confusion_matrix, classification_report, roc_auc_score
from imblearn.over_sampling import RandomOverSampler
import joblib
from pathlib import Path
import warnings

def main():
    warnings.filterwarnings('ignore')

    base_dir = Path(__file__).resolve().parent
    data_path = base_dir / 'data' / 'lung_cancer.csv'
    models_dir = base_dir / 'models'
    models_dir.mkdir(exist_ok=True)

    try:
        df = pd.read_csv(data_path)
        df.columns = df.columns.str.strip()
    except FileNotFoundError:
        print("错误：未找到数据文件 lung_cancer.csv")
        return

    expected_columns = ['GENDER', 'AGE', 'SMOKING', 'YELLOW_FINGERS', 'ANXIETY',
                        'PEER_PRESSURE', 'CHRONIC DISEASE', 'FATIGUE', 'ALLERGY',
                        'WHEEZING', 'ALCOHOL CONSUMING', 'COUGHING',
                        'SHORTNESS OF BREATH', 'SWALLOWING DIFFICULTY',
                        'CHEST PAIN', 'LUNG_CANCER']
    if set(expected_columns) != set(df.columns):
        print("字段不匹配：", df.columns.tolist())
        return

    # 标签编码
    encoder = LabelEncoder()
    df['LUNG_CANCER'] = encoder.fit_transform(df['LUNG_CANCER'].str.strip())  # YES/NO -> 1/0
    df['GENDER'] = encoder.fit_transform(df['GENDER'].str.strip())  # M/F -> 1/0

    # **对部分特征进行减1处理，使它们从{1,2}变为{0,1}**
    cols_to_subtract_1 = ['SMOKING', 'YELLOW_FINGERS', 'ANXIETY', 'PEER_PRESSURE',
                         'CHRONIC DISEASE', 'FATIGUE', 'ALLERGY', 'WHEEZING',
                         'ALCOHOL CONSUMING', 'COUGHING', 'SHORTNESS OF BREATH',
                         'SWALLOWING DIFFICULTY', 'CHEST PAIN']
    for col in cols_to_subtract_1:
        df[col] = df[col] - 1

    X = df.drop('LUNG_CANCER', axis=1)
    y = df['LUNG_CANCER']

    # 过采样处理
    X_over, y_over = RandomOverSampler(random_state=42).fit_resample(X, y)

    # 划分训练测试集
    X_train, X_test, y_train, y_test = train_test_split(
        X_over, y_over, test_size=0.2, random_state=42, stratify=y_over
    )

    # 标准化 AGE
    scaler = StandardScaler()
    X_train['AGE'] = scaler.fit_transform(X_train[['AGE']])
    X_test['AGE'] = scaler.transform(X_test[['AGE']])

    # 使用随机森林 + 概率校准
    rf = RandomForestClassifier(n_estimators=100, random_state=42)
    calibrated_clf = CalibratedClassifierCV(rf, cv=5)
    calibrated_clf.fit(X_train, y_train)

    # 模型评估
    y_pred = calibrated_clf.predict(X_test)
    y_proba = calibrated_clf.predict_proba(X_test)[:, 1]
    print("分类报告：\n", classification_report(y_test, y_pred))
    print("混淆矩阵：\n", confusion_matrix(y_test, y_pred))
    print(f"ROC AUC: {roc_auc_score(y_test, y_proba):.4f}")

    # 保存模型和标准化器
    joblib.dump(calibrated_clf, models_dir / 'best_lung_cancer_model.pkl')
    joblib.dump(scaler, models_dir / 'scaler.pkl')
    print("模型和标准化器已保存到 models/ 目录。")

    # 测试样本
    test_samples = [
        [1, 70, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1],
    ]
    df_test = pd.DataFrame(test_samples, columns=X.columns)

    # 同样对测试数据做减1处理
    for col in cols_to_subtract_1:
        df_test[col] = df_test[col] - 1

    # 标准化 AGE
    df_test['AGE'] = scaler.transform(df_test[['AGE']])

    print(">>> 测试样本预测结果：")
    for i, row in df_test.iterrows():
        pred = calibrated_clf.predict([row])[0]
        proba = calibrated_clf.predict_proba([row])[0, 1]
        label = "肺癌" if pred == 1 else "非肺癌"
        print(f"样本{i}预测结果：{label}，肺癌概率：{proba:.4f}")

if __name__ == "__main__":
    main()
