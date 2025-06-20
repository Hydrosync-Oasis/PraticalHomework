from flask import Blueprint, request, jsonify
import pandas as pd
import joblib

def create_predict_bp(model_path='./models/best_lung_cancer_model.pkl', scaler_path='./models/scaler.pkl'):
    predict_bp = Blueprint('predict_bp', __name__)

    # 加载模型和标准化器
    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)

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
        # 转换字典键名为表头列名，只取模型训练时用的字段
        data_mapped = {COLUMN_MAP[k]: v for k, v in data_dict.items() if k in COLUMN_MAP}
        df_input = pd.DataFrame([data_mapped])

        # 性别映射 M=1, F=0
        df_input['GENDER'] = df_input['GENDER'].map({'M': 1, 'F': 0})

        # 除了GENDER和AGE的列都减1（训练时做的）
        for col in df_input.columns:
            if col not in ['GENDER', 'AGE']:
                df_input[col] = df_input[col] - 1

        # 年龄标准化
        df_input['AGE'] = scaler.transform(df_input[['AGE']])
        return df_input

    @predict_bp.route('/predict', methods=['POST'])
    def predict():
        data = request.json
        if not data:
            return jsonify({'error': '无效输入'}), 400
        try:
            print("输入数据（原始）：", data)

            processed = preprocess_input(data)
            print("预处理后数据：\n", processed)

            pred = model.predict(processed)
            print("预测结果：", pred)

            proba = model.predict_proba(processed)
            print("预测概率：", proba)

            return jsonify({
                'prediction': int(pred[0]),
                'prediction_label': '肺癌' if pred[0] == 1 else '非肺癌',
                'probability': float(proba[0, 1])  # 返回患肺癌的概率
            })

        except Exception as e:
            return jsonify({'error': str(e)}), 500

    return predict_bp
