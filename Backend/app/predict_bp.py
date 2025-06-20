from flask import Blueprint, request, jsonify
import pandas as pd

def create_predict_bp(model, scaler):
    predict_bp = Blueprint('predict_bp', __name__)

    def preprocess_input(data_dict):
        df_input = pd.DataFrame([data_dict])
        df_input.columns = df_input.columns.str.upper()  # 👈 把小写字段变成大写（GENDER）

        # ✅ 将带下划线的列名改为模型使用的“带空格”字段名
        column_mapping = {
            "YELLOW_FINGERS": "YELLOW FINGERS",
            "PEER_PRESSURE": "PEER PRESSURE",
            "CHRONIC_DISEASE": "CHRONIC DISEASE",
            "ALCOHOL_CONSUMING": "ALCOHOL CONSUMING",
            "SHORTNESS_OF_BREATH": "SHORTNESS OF BREATH",
            "SWALLOWING_DIFFICULTY": "SWALLOWING DIFFICULTY",
            "CHEST_PAIN": "CHEST PAIN"
        }
        df_input.rename(columns=column_mapping, inplace=True)

        # ✅ 性别映射
        df_input['GENDER'] = df_input['GENDER'].map({'M': 1, 'F': 0})

        # ✅ 除 AGE、GENDER 外，其他字段都进行 -1 处理
        for col in df_input.columns:
            if col not in ['GENDER', 'AGE']:
                df_input[col] = df_input[col] - 1

        # ✅ 年龄标准化
        df_input['AGE'] = scaler.transform(df_input[['AGE']])
        return df_input

    @predict_bp.route('/predict', methods=['POST'])
    def predict():
        data = request.json
        if not data:
            return jsonify({'error': '无效输入'}), 400
        try:
            processed = preprocess_input(data)
            pred = model.predict(processed)[0]
            proba = model.predict_proba(processed)[0, 1]
            return jsonify({
                'prediction': int(pred),
                'prediction_label': '肺癌' if pred == 1 else '非肺癌',
                'probability': float(proba)
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    return predict_bp
