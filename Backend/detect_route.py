from flask import Blueprint, request, jsonify
import os
from datetime import datetime
from werkzeug.utils import secure_filename
from PIL import Image
from app.yolo_model import model  # 确保模型能正常加载

detect_bp = Blueprint('detect', __name__)

UPLOAD_FOLDER = 'static/uploads'
DETECT_FOLDER = 'static/detections'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DETECT_FOLDER, exist_ok=True)

@detect_bp.route('/yolo_detect', methods=['POST'])
def upload_and_detect():
    try:
        image_file = request.files.get("image")
        if not image_file:
            return jsonify({"error": "No image uploaded"}), 400

        filename = datetime.now().strftime("%Y%m%d%H%M%S") + "_" + secure_filename(image_file.filename)
        upload_path = os.path.join(UPLOAD_FOLDER, filename)
        detect_path = os.path.join(DETECT_FOLDER, filename)

        image_file.save(upload_path)

        # 检查是否为有效图像
        try:
            Image.open(upload_path).verify()
        except Exception as e:
            return jsonify({"error": f"Invalid image: {str(e)}"}), 400

        # 模型推理
        results = model(upload_path)
        result_img_array = results[0].plot()
        Image.fromarray(result_img_array).save(detect_path)

        detections = []
        boxes = results[0].boxes
        if boxes is not None and boxes.cls.numel() > 0:
            for cls_id, conf in zip(boxes.cls, boxes.conf):
                class_name = model.names[int(cls_id)]
                confidence = round(float(conf) * 100, 2)
                detections.append(f"{class_name}: {confidence}%")
        else:
            detections.append("No objects detected.")

        return jsonify({
            "message": "Detection complete",
            "detections": detections,
            "image_path": f"/static/detections/{filename}"
        })

    except Exception as e:
        print("❌ Exception caught:", e)
        return jsonify({"error": str(e)}), 500
