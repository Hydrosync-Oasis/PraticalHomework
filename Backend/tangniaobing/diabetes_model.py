import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, roc_curve, auc
import joblib  # 用于模型保存和加载

# 全局变量
scaler = StandardScaler()
model = LogisticRegression()

def train_model(data_path="diabetes.csv", model_path="diabetes_model.pkl", scaler_path="scaler.pkl"):
    # 1. 读取数据
    df = pd.read_csv(data_path)

    # 2. 替换0为NaN并填充均值
    cols_with_zeros = ["Glucose", "BloodPressure", "SkinThickness", "Insulin", "BMI"]
    df[cols_with_zeros] = df[cols_with_zeros].replace(0, np.nan)
    df.fillna(df.mean(), inplace=True)

    # 3. 分离特征与标签
    X = df.drop("Outcome", axis=1)
    y = df["Outcome"]

    # 4. 标准化
    X_scaled = scaler.fit_transform(X)

    # 5. 划分数据集
    x_train, x_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

    # 6. 模型训练
    model.fit(x_train, y_train)

    # 7. 模型评估
    y_pred = model.predict(x_test)
    y_prob = model.predict_proba(x_test)[:, 1]
    fpr, tpr, _ = roc_curve(y_test, y_prob)
    roc_auc = auc(fpr, tpr)

    print("准确率：", accuracy_score(y_test, y_pred))
    print("混淆矩阵：\n", confusion_matrix(y_test, y_pred))
    print("分类报告：\n", classification_report(y_test, y_pred))

    # 8. 绘制 ROC 曲线
    plt.figure(figsize=(8,6))
    plt.plot(fpr, tpr, label=f'ROC曲线 (AUC = {roc_auc:.2f})')
    plt.plot([0, 1], [0, 1], 'k--')
    plt.xlabel("假阳性率")
    plt.ylabel("真正率")
    plt.title("逻辑回归 ROC 曲线")
    plt.legend()
    plt.grid()
    plt.show()

    # 9. 保存模型与标准化器
    joblib.dump(model, model_path)
    joblib.dump(scaler, scaler_path)

def predict_samples(samples, model_path="diabetes_model.pkl", scaler_path="scaler.pkl"):
    # 加载模型与Scaler
    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)

    # 转为NumPy数组并标准化
    test_samples = np.array(samples)
    test_samples_scaled = scaler.transform(test_samples)

    # 模型预测
    predictions = model.predict(test_samples_scaled)
    probabilities = model.predict_proba(test_samples_scaled)[:, 1]

    # 返回结果
    results = []
    for i, (pred, prob) in enumerate(zip(predictions, probabilities), 1):
        result = "糖尿病" if pred == 1 else "未患糖尿病"
        results.append({
            "样本编号": i,
            "预测结果": result,
            "概率": round(prob, 2)
        })
    return results
