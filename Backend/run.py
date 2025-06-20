from flask import Flask
import joblib
from app.predict_bp import create_predict_bp

model = joblib.load('models/best_lung_cancer_model.pkl')
scaler = joblib.load('models/scaler.pkl')

app = Flask(__name__)

predict_bp = create_predict_bp(model, scaler)
app.register_blueprint(predict_bp, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True)
