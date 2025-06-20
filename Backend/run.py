from flask import Flask
from flask_cors import CORS
from app.predict_bp import create_predict_bp

app = Flask(__name__)

CORS(app, resources={r"/api/*": {"origins": "http://localhost:8080"}})

# 不传入参数，蓝图内自动加载模型和 scaler
predict_bp = create_predict_bp()
app.register_blueprint(predict_bp, url_prefix='/api')

@app.route('/')
def home():
    return 'Lung Cancer Prediction API is running. Visit /api/predict to use the model.'

if __name__ == '__main__':
    app.run(debug=True)
