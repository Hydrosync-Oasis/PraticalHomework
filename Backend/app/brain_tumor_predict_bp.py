# Backend/app/brain_tumor_predict_bp.py

from flask import Blueprint, request, jsonify
from tensorflow.keras.models import load_model
import numpy as np
import cv2
import os

brain_bp = Blueprint('brain_bp', __name__)

# 加载模型（路径根据你的目录调整）
model_path = os.path.join(os.path.dirname(__file__), '..', 'models', 'brain_tumor_model.h5')
model = load_model(model_path)

@brain_bp.route('/predict/brain_tumor', methods=['POST'])
def predict_brain_tumor():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    file = request.files['image']
    image = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)

    if image is None:
        return jsonify({'error': 'Invalid image'}), 400

    # 图像预处理
    image = cv2.resize(image, (128, 128))
    image = image.astype('float32') / 127.5 - 1.0
    image = np.expand_dims(image, axis=0)

    prob = float(model.predict(image)[0][0])

    return jsonify({
        'filename': file.filename,
        'tumor_probability': round(prob, 4),
        'predicted_label': 'Tumor' if prob >= 0.5 else 'No Tumor'
    })
