from flask import Flask
import joblib
from flask_cors import CORS
from app.predict_bp import create_predict_bp

model = joblib.load('models/best_lung_cancer_model.pkl')
scaler = joblib.load('models/scaler.pkl')

app = Flask(__name__)

CORS(app, resources={r"/api/*": {"origins": "http://localhost:8080"}})

predict_bp = create_predict_bp(model, scaler)
app.register_blueprint(predict_bp, url_prefix='/api')

@app.route('/')
def home():
    return 'Lung Cancer Prediction API is running. Visit /api/predict to use the model.'

if __name__ == '__main__':
    app.run(debug=True)
