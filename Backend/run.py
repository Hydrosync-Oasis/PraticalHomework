<<<<<<< HEAD
from flask import Flask, jsonify
from flask_cors import CORS
from tangniaobing.diabetes_predict_bp import diabetes_predict_bp  # 糖尿病预测蓝图
from app.predict_bp import create_predict_bp  # 肺癌预测蓝图工厂
from analysis import create_analysis_bp      # 分析蓝图工厂
from app.brain_tumor_predict_bp import brain_bp  # 脑肿瘤预测蓝图

from app.apis.boxplot_api import boxplot_api
from app.apis.scatter_bmi_api import scatter_bmi_api
from app.apis.age_hist_api import age_hist_api
from app.apis.region_avg_api import region_avg_api
from app.apis.scatter_age_api import scatter_age_api
from app.apis.correlation_api import correlation_api

=======
# run.py

from flask import Flask
from flask_cors import CORS

# 模块蓝图导入
from tangniaobing.diabetes_predict_bp import diabetes_predict_bp         # /api/diabetes_predict
from app.predict_bp import create_predict_bp                             # /api/predict
from analysis import create_analysis_bp                                  # /api/analysis
from app.brain_tumor_predict_bp import brain_bp                          # /api/brain_tumor_predict
from detect_route import detect_bp                                   # /api/yolo_detect
>>>>>>> 1e9dd948fd57a917e206c53c2c4f8ac4d513524a

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

<<<<<<< HEAD
app.register_blueprint(boxplot_api, url_prefix='/api/analysis/boxplot')
app.register_blueprint(scatter_bmi_api, url_prefix='/api/analysis/scatter_bmi')
app.register_blueprint(age_hist_api, url_prefix='/api/analysis/age_hist')
app.register_blueprint(region_avg_api, url_prefix='/api/analysis/region_avg')
app.register_blueprint(scatter_age_api, url_prefix='/api/analysis/scatter_age')
app.register_blueprint(correlation_api, url_prefix='/api/analysis/correlation')
=======
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
>>>>>>> 1e9dd948fd57a917e206c53c2c4f8ac4d513524a

if __name__ == '__main__':
    app.run(debug=True)
