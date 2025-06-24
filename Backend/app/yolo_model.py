# app/yolo_model.py

import os
from ultralytics import YOLO

# 获取模型路径（相对项目根目录）
model_path = os.path.join('models', 'best.pt')

# 检查模型文件是否存在
if not os.path.exists(model_path):
    raise FileNotFoundError(f"模型文件未找到: {model_path}")

# 加载 YOLOv8 模型（默认使用 CPU）
model = YOLO(model_path)
