from flask import Blueprint, request, jsonify
import traceback
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
