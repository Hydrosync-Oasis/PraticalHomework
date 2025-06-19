import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, classification_report, roc_curve, roc_auc_score


def print_confusion_and_report(model, X_test, y_test):
    """
    打印混淆矩阵和分类报告
    """
    y_pred = model.predict(X_test)
    cm = confusion_matrix(y_test, y_pred)

    print("混淆矩阵：")
    print(cm)
    print("\n分类报告：")
    print(classification_report(y_test, y_pred))

    plt.figure(figsize=(5, 4))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Oranges')
    plt.xlabel("预测值")
    plt.ylabel("真实值")
    plt.title("混淆矩阵")
    plt.show()


def plot_roc_curve(y_test, y_pred_proba, model_name="模型"):
    """
    绘制ROC曲线和计算AUC
    """
    fpr, tpr, _ = roc_curve(y_test, y_pred_proba)
    auc_score = roc_auc_score(y_test, y_pred_proba)

    plt.figure(figsize=(6, 6))
    plt.plot(fpr, tpr, color='green', lw=2, label=f'{model_name} (AUC = {auc_score:.4f})')
    plt.plot([0, 1], [0, 1], color='gray', linestyle='--')
    plt.title(f"{model_name} 的 ROC 曲线")
    plt.xlabel("假阳性率 (False Positive Rate)")
    plt.ylabel("真阳性率 (True Positive Rate)")
    plt.legend(loc='lower right')
    plt.grid(True)
    plt.show()
