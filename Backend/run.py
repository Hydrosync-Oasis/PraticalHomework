from flask import Flask, request, jsonify
from flask_cors import CORS
from diabetes_model import train_model, predict_samples
from app.predict_bp import create_predict_bp
from analysis import create_analysis_bp
import traceback

app = Flask(__name__)

# CORS配置
CORS(app, resources={
    r"/api/*": {"origins": "http://localhost:8080"},
    r"/train": {"origins": "*"},
    r"/predict": {"origins": "*"},
    r"/predict_1": {"origins": "*"},
    r"/": {"origins": "*"},
})

# 注册肺癌预测蓝图，路径前缀/api
predict_bp = create_predict_bp()
app.register_blueprint(predict_bp, url_prefix='/api')

# 注册数据分析蓝图
analysis_bp = create_analysis_bp()
app.register_blueprint(analysis_bp, url_prefix='/api/analysis')

# 糖尿病模型训练接口
@app.route('/train', methods=['POST'])
def train():
    try:
        train_model()
        return jsonify({"message": "糖尿病模型训练完成并已保存。"})
    except Exception as e:
        return jsonify({"error": str(e), "trace": traceback.format_exc()}), 500

# 糖尿病模型预测接口，改名predict_1
@app.route('/predict_1', methods=['POST'])
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

# 根路径简单返回提示
@app.route('/')
def home():
    return 'API 服务已启动。肺癌预测接口: /api/predict  糖尿病预测接口: /predict_1'

if __name__ == '__main__':
    app.run(debug=True)
