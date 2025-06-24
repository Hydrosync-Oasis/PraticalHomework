# run.py

from flask import Flask
from flask_cors import CORS

# 模块蓝图导入
from tangniaobing.diabetes_predict_bp import diabetes_predict_bp         # /api/diabetes_predict
from app.predict_bp import create_predict_bp                             # /api/predict
from analysis import create_analysis_bp                                  # /api/analysis
from app.brain_tumor_predict_bp import brain_bp                          # /api/brain_tumor_predict
from detect_route import detect_bp                                   # /api/yolo_detect

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0  # 禁用浏览器缓存（用于图像等静态资源）

# CORS 设置（前端跨域支持）
CORS(app, resources={r"/api/*": {"origins": "*"}})

# ✅ 注册蓝图（全为 POST 风格 API）
app.register_blueprint(create_predict_bp(), url_prefix='/api/predict')          # 肺癌预测
app.register_blueprint(diabetes_predict_bp, url_prefix='/api/diabetes_predict') # 糖尿病预测
app.register_blueprint(brain_bp, url_prefix='/api/brain_tumor_predict')         # 脑部肿瘤预测
app.register_blueprint(create_analysis_bp(), url_prefix='/api/analysis')        # 数据分析
app.register_blueprint(detect_bp, url_prefix='/api')                            # 图像检测（YOLO）

@app.route('/')
def home():
    return (
        '✅ API 服务已启动：<br>'
        '<ul>'
        '<li><strong>POST</strong> /api/predict - 肺癌预测</li>'
        '<li><strong>POST</strong> /api/diabetes_predict - 糖尿病预测</li>'
        '<li><strong>POST</strong> /api/brain_tumor_predict - 脑部肿瘤预测（图像）</li>'
        '<li><strong>POST</strong> /api/yolo_detect - 通用图像目标检测（YOLO）</li>'
        '<li><strong>POST</strong> /api/analysis/... - 数据分析模块</li>'
        '</ul>'
    )

if __name__ == '__main__':
    app.run(debug=True)
