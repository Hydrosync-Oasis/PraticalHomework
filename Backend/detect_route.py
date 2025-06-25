from flask import Blueprint, request, send_file
import os
from datetime import datetime
from werkzeug.utils import secure_filename
from PIL import Image
from app.yolo_model import model

detect_bp = Blueprint('detect', __name__)

UPLOAD_FOLDER = 'static/uploads'
DETECT_FOLDER = 'static/detections'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DETECT_FOLDER, exist_ok=True)

@detect_bp.route('/yolo_detect', methods=['POST'])
def upload_and_detect():
    image_file = request.files.get("image")
    if image_file:
        # 保存上传图像
        filename = datetime.now().strftime("%Y%m%d%H%M%S") + "_" + secure_filename(image_file.filename)
        upload_path = os.path.join(UPLOAD_FOLDER, filename)
        detect_path = os.path.join(DETECT_FOLDER, filename)
        image_file.save(upload_path)

        # 模型推理并绘图
        results = model(upload_path)
        result_img_array = results[0].plot()
        result_img = Image.fromarray(result_img_array)
        result_img.save(detect_path)

        # 返回处理后的图片
        return send_file(detect_path, mimetype='image/jpeg')

    return "No image uploaded", 400
