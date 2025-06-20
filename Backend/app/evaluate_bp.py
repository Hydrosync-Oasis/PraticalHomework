from flask import Blueprint, request, jsonify
import pandas as pd
from sklearn.metrics import confusion_matrix, classification_report

evaluate_bp = Blueprint('evaluate_bp', __name__)

# 模型同样需要外部加载并传入或在此加载（示例用全局变量）
model = None

@evaluate_bp.route('/evaluate', methods=['POST'])
def evaluate():
    data = request.json
    if not data or 'X_test' not in data or 'y_test' not in data:
        return jsonify({'error': '需要提供X_test和y_test'}), 400
    try:
        X_test = pd.DataFrame(data['X_test'])
        y_test = pd.Series(data['y_test'])
        y_pred = model.predict(X_test)

        cm = confusion_matrix(y_test, y_pred).tolist()
        report = classification_report(y_test, y_pred, output_dict=True)

        return jsonify({'confusion_matrix': cm, 'classification_report': report})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
