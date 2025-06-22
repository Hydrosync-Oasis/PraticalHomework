from flask import Flask, jsonify
from flask_cors import CORS
from tangniaobing.diabetes_predict_bp import diabetes_predict_bp  # 新导入
from tangniaobing.diabetes_model import train_model
from app.predict_bp import create_predict_bp
from analysis import create_analysis_bp
import traceback
from app.brain_tumor_predict_bp import brain_bp  # 导入脑肿瘤预测蓝图



app = Flask(__name__)

# CORS配置
CORS(app, resources={
    r"/api/*": {"origins": "http://localhost:8080"},
    r"/train": {"origins": "*"},
    r"/predict_1": {"origins": "*"},
    r"/": {"origins": "*"},
})

# 注册蓝图
app.register_blueprint(diabetes_predict_bp)  # 注册糖尿病预测蓝图，默认路径 /predict_1
predict_bp = create_predict_bp()
app.register_blueprint(predict_bp, url_prefix='/api')
analysis_bp = create_analysis_bp()
app.register_blueprint(analysis_bp, url_prefix='/api/analysis')
app.register_blueprint(brain_bp, url_prefix='/api')


@app.route('/')
def home():
    return 'API 服务已启动。肺癌预测接口: /api/predict  糖尿病预测接口: /predict_1  脑部肿瘤预测接口: /api/brain_tumor'

if __name__ == '__main__':
    app.run(debug=True)
