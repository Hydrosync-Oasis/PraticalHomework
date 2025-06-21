from flask import Blueprint, request, jsonify
import traceback
import sys
import os

# 添加当前文件目录到 sys.path，确保能找到同目录的 diabetes_model.py
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from diabetes_model import predict_samples

diabetes_predict_bp = Blueprint('diabetes_predict_bp', __name__)

@diabetes_predict_bp.route('/predict_1', methods=['POST'])
def predict_1():
    try:
        data = request.json
        samples = data.get("samples", [])

        if not samples or not isinstance(samples, list):
            return jsonify({"error": "请输入有效的测试样本列表。"}), 400

        results = predict_samples(samples)
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e), "trace": traceback.format_exc()}), 500
