# Backend/app/brain_tumor_predict_bp.py

from flask import Blueprint, request, jsonify
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
import numpy as np
import cv2
import os
import traceback

brain_bp = Blueprint('brain_bp', __name__)

# 标签映射（确保与训练一致）
label_names = {0: "Glioma", 1: "Meningioma", 2: "Pituitary", 3: "No Tumor"}

# 加载模型
model_path = os.path.join(os.path.dirname(__file__), '..', 'models', 'cnn_brain_tumor_model.h5')
model = load_model(model_path)

@brain_bp.route('/predict/brain_tumor', methods=['POST'])
def predict_brain_tumor():
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image uploaded'}), 400

        file = request.files['image']
        image_bytes = file.read()
        image = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR)

        if image is None:
            return jsonify({'error': 'Invalid image format'}), 400

        # BGR转RGB，MobileNetV2预处理期望RGB输入
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # 图像预处理（与训练保持一致）
        image = cv2.resize(image, (128, 128))
        image = image.astype('float32')
        image = preprocess_input(image)  # 使用 MobileNetV2 的预处理
        image = np.expand_dims(image, axis=0)  # 扩展维度 [1, 128, 128, 3]

        # 模型预测
        probs = model.predict(image)[0]
        pred_index = int(np.argmax(probs))
        pred_label = label_names[pred_index]

        # 构建响应
        return jsonify({
            'filename': file.filename,
            'predicted_label': pred_label,
            'probability': {label_names[i]: round(float(p), 4) for i, p in enumerate(probs)},
            'predicted_index': pred_index
        })
    except Exception as e:
        return jsonify({
            'error': 'Prediction failed',
            'message': str(e),
            'traceback': traceback.format_exc()
        }), 500

