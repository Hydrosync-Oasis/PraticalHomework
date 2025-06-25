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
app.register_blueprint(brain_bp, url_prefix='/api')  # /api/brain_tumor_predict

app.register_blueprint(boxplot_api, url_prefix='/api/analysis/boxplot')
app.register_blueprint(scatter_bmi_api, url_prefix='/api/analysis/scatter_bmi')
app.register_blueprint(age_hist_api, url_prefix='/api/analysis/age_hist')
app.register_blueprint(region_avg_api, url_prefix='/api/analysis/region_avg')
app.register_blueprint(scatter_age_api, url_prefix='/api/analysis/scatter_age')
app.register_blueprint(correlation_api, url_prefix='/api/analysis/correlation')

if __name__ == '__main__':
    app.run(debug=True)
