from flask import Flask, jsonify
from flask_cors import CORS
from tangniaobing.diabetes_predict_bp import diabetes_predict_bp  # 糖尿病预测蓝图
from tangniaobing.diabetes_model import train_model
from app.predict_bp import create_predict_bp  # 肺癌预测蓝图工厂
from analysis import create_analysis_bp      # 分析蓝图工厂
from app.brain_tumor_predict_bp import brain_bp  # 脑肿瘤预测蓝图

import traceback

app = Flask(__name__)

# CORS配置
CORS(app, resources={
    r"/api/*": {"origins": "http://localhost:8080"},
    r"/train": {"origins": "*"},
    r"/predict_1": {"origins": "*"},
    r"/": {"origins": "*"},
})

# 注册蓝图
app.register_blueprint(diabetes_predict_bp)  # /predict_1
predict_bp = create_predict_bp()
app.register_blueprint(predict_bp, url_prefix='/api')  # /api/predict
analysis_bp = create_analysis_bp()
app.register_blueprint(analysis_bp, url_prefix='/api/analysis')  # /api/analysis/...
app.register_blueprint(brain_bp, url_prefix='/api')  # 脑肿瘤接口，比如 /api/brain_tumor_predict

@app.route('/')
def home():
    return ('API 服务已启动。'
            '肺癌预测接口: /api/predict  '
            '糖尿病预测接口: /predict_1  '
            '脑部肿瘤预测接口: /api/brain_tumor_predict')

if __name__ == '__main__':
    app.run(debug=True)
