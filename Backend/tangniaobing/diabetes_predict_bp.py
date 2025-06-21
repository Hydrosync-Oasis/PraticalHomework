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
        data = request.json  # 获取请求体

        if data is None:
            return jsonify({"error": "请求体不能为空"}), 400

        # 支持单个样本 dict，或者多个样本 list
        if isinstance(data, dict):
            samples = [data]  # 单个样本，包装成列表
        elif isinstance(data, list):
            samples = data  # 多个样本直接用
            # 验证列表中每项都是 dict
            if not all(isinstance(item, dict) for item in samples):
                return jsonify({"error": "列表中所有样本应为字典格式"}), 400
        else:
            return jsonify({"error": "请求体应为样本字典或样本字典列表"}), 400

        results = predict_samples(samples)
        return jsonify(results)

    except Exception as e:
        return jsonify({
            "error": str(e),
            "trace": traceback.format_exc()
        }), 500



