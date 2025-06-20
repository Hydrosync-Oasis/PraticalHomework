from flask import Flask
import joblib
from app.predict_bp import create_predict_bp
from analysis import create_analysis_bp
from flask_cors import CORS

model = joblib.load('models/best_lung_cancer_model.pkl')
scaler = joblib.load('models/scaler.pkl')

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # 允许跨域请求

# 注册预测 API 路由
predict_bp = create_predict_bp(model, scaler)
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