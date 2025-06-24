import os
from flask import Blueprint, request, render_template
from werkzeug.utils import secure_filename
from datetime import datetime
from PIL import Image
from app.yolo_model import model  #  正确：从 app 模块导入



detect_bp = Blueprint('detect', __name__)

# 配置上传和保存目录
UPLOAD_FOLDER = 'static/uploads'
DETECT_FOLDER = 'static/detections'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DETECT_FOLDER, exist_ok=True)

@detect_bp.route('/yolo_detect', methods=['POST'])
def upload_and_detect():
    if request.method == 'POST':
        image_file = request.files.get("image")
        if image_file:
            filename = datetime.now().strftime("%Y%m%d%H%M%S") + "_" + secure_filename(image_file.filename)
            upload_path = os.path.join(UPLOAD_FOLDER, filename)
            detect_path = os.path.join(DETECT_FOLDER, filename)

            image_file.save(upload_path)

            # 使用模型进行目标检测
            # 载入图像并推理
            results = model(upload_path)  # 直接调用模型本身而不是 .predict()
            # 获取绘图图像
            result_img_array = results[0].plot()
            Image.fromarray(result_img_array).save(detect_path)

            # 提取检测结果（标签+置信度）
            detections = []
            boxes = results[0].boxes
            if boxes is not None and boxes.cls.numel() > 0:
                for cls_id, conf in zip(boxes.cls, boxes.conf):
                    class_name = model.names[int(cls_id)]
                    confidence = round(float(conf) * 100, 2)
                    detections.append(f"{class_name}: {confidence}%")
            else:
                detections.append("No objects detected.")

            return render_template(
                'index.html',
                prediction="Detection Complete",
                detections=detections,
                image_path=f"detections/{filename}"
            )

    return render_template('index.html', prediction=None)
