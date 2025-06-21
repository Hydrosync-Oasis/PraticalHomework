from flask import Flask, request, jsonify
from Backend.tangniaobing.diabetes_model import train_model, predict_samples
import traceback

app = Flask(__name__)

@app.route('/train', methods=['POST'])
def train():
    try:
        train_model()
        return jsonify({"message": "模型训练完成并已保存。"})
    except Exception as e:
        return jsonify({"error": str(e), "trace": traceback.format_exc()}), 500

@app.route('/predict', methods=['POST'])
def predict_1():
    try:
        data = request.json
        if not data:
            return jsonify({"error": "请输入有效的测试样本。"}), 400

        # 支持单个样本dict，或者多个样本列表
        if isinstance(data, dict):
            samples = [data]
        elif isinstance(data, list):
            samples = data
        else:
            return jsonify({"error": "输入格式错误，应为字典或列表。"}), 400

        results = predict_samples(samples)
        return jsonify(results)

    except Exception as e:
        return jsonify({"error": str(e), "trace": traceback.format_exc()}), 500

if __name__ == '__main__':
    app.run(debug=True)
