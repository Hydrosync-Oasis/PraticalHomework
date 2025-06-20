from flask import Blueprint, request, jsonify
import pandas as pd

def create_predict_bp(model, scaler):
    predict_bp = Blueprint('predict_bp', __name__)

    # 映射前端字段 -> 表头字段
    COLUMN_MAP = {
        "gender": "GENDER",
        "age": "AGE",
        "smoking": "SMOKING",
        "yellow_fingers": "YELLOW_FINGERS",
        "anxiety": "ANXIETY",
        "peer_pressure": "PEER_PRESSURE",
        "chronic_disease": "CHRONIC DISEASE",
        "fatigue": "FATIGUE",
        "allergy": "ALLERGY",
        "wheezing": "WHEEZING",
        "alcohol_consuming": "ALCOHOL CONSUMING",
        "coughing": "COUGHING",
        "shortness_of_breath": "SHORTNESS OF BREATH",
        "swallowing_difficulty": "SWALLOWING DIFFICULTY",
        "chest_pain": "CHEST PAIN"
    }

    def preprocess_input(data_dict):
        # 转换字典键名为表头列名
        data_mapped = {COLUMN_MAP[k]: v for k, v in data_dict.items() if k in COLUMN_MAP}
        df_input = pd.DataFrame([data_mapped])

        # 性别映射
        df_input['GENDER'] = df_input['GENDER'].map({'M': 1, 'F': 0})

        # 除了GENDER和AGE的列都减1（假设数据都是从1开始编码）
        for col in df_input.columns:
            if col not in ['GENDER', 'AGE']:
                df_input[col] = df_input[col] - 1

        # 标准化年龄
        df_input['AGE'] = scaler.transform(df_input[['AGE']])
        return df_input

    @predict_bp.route('/predict', methods=['POST'])
    @predict_bp.route('/predict', methods=['POST'])
    def predict():
        data = request.json
        if not data:
            return jsonify({'error': '无效输入'}), 400
        try:
            print("输入数据（原始）：", data)  # 打印原始前端传入数据

            processed = preprocess_input(data)
            print("预处理后数据：\n", processed)  # 打印预处理后的 DataFrame

            pred = model.predict(processed)
            print("预测结果：", pred)  # 打印预测的类别

            proba = model.predict_proba(processed)
            print("预测概率：", proba)  # 打印预测的概率分布

            return jsonify({
                'prediction': int(pred[0]),
                'prediction_label': '肺癌' if pred[0] == 1 else '非肺癌',
                'probability': float(proba[0, 1])
            })

        except Exception as e:
            return jsonify({'error': str(e)}), 500

    return predict_bp
