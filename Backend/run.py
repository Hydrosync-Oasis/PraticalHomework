from flask import Flask
from flask_cors import CORS
from app.predict_bp import create_predict_bp
from analysis import create_analysis_bp

app = Flask(__name__)

# 合并两种CORS配置
CORS(app, resources={
    r"/*": {"origins": "*"},  # 允许所有来源访问所有路由
    r"/api/*": {"origins": "http://localhost:8080"}  # 允许localhost:8080访问/api/*路由
})

# 使用修改后的create_predict_bp，不需要传入模型和scaler参数
predict_bp = create_predict_bp()
app.register_blueprint(predict_bp, url_prefix='/api')

# 注册数据分析 API 路由
analysis_bp = create_analysis_bp()
app.register_blueprint(analysis_bp, url_prefix='/api/analysis')

# 添加主页路由，避免 404
@app.route('/')
def home():
    return 'Lung Cancer Prediction API is running. Visit /api/predict to use the model.'

if __name__ == '__main__':
    app.run(debug=True)