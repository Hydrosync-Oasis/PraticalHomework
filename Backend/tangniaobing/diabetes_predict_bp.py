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
        samples = data.get("samples", None)

        if samples is None:
            return jsonify({"error": "请输入有效的测试样本。"}), 400

        # 如果是单个样本 dict，转换为列表包裹
        if isinstance(samples, dict):
            samples = [samples]
        elif not isinstance(samples, list):
            return jsonify({"error": "samples 应为字典或列表类型。"}), 400

        results = predict_samples(samples)
        return jsonify(results)

    except Exception as e:
        return jsonify({
            "error": str(e),
            "trace": traceback.format_exc()
        }), 500

