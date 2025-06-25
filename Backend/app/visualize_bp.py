from flask import Blueprint, jsonify, request
import matplotlib.pyplot as plt
import io
import base64

#  关键导入：从 utils 包导入自定义绘图函数
from utils.visualize import (
    plot_age_distribution,
    plot_categorical_counts,
    plot_correlation_heatmap,
    plot_gender_cancer_counts,
    plot_age_group_stacked_bar,
    plot_smoking_boxplot,
    plot_sample_counts_before_after_sampling
)

visualize_bp = Blueprint('visualize_bp', __name__)

def fig_to_base64(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    img_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    plt.close(fig)
    return img_base64

# ✅ 全局 df 变量，用于测试；运行前你必须在主程序中赋值
df = None

@visualize_bp.route('/visualize/age_distribution', methods=['GET'])
def viz_age_distribution():
    fig = plt.figure(figsize=(20, 6))
    plot_age_distribution(df)
    return jsonify({'image': fig_to_base64(fig)})

@visualize_bp.route('/visualize/categorical_counts', methods=['GET'])
def viz_categorical_counts():
    cat_cols = request.args.get('cat_cols')
    if cat_cols:
        cat_cols = cat_cols.split(',')
    else:
        cat_cols = [
            'GENDER', 'SMOKING', 'YELLOW_FINGERS', 'ANXIETY', 'PEER_PRESSURE',
            'CHRONIC DISEASE', 'FATIGUE', 'ALLERGY', 'WHEEZING',
            'ALCOHOL CONSUMING', 'COUGHING', 'SHORTNESS OF BREATH',
            'SWALLOWING DIFFICULTY', 'CHEST PAIN'
        ]
    fig = plt.figure(figsize=(30, 5 * len(cat_cols)))
    plot_categorical_counts(df, cat_cols)
    return jsonify({'image': fig_to_base64(fig)})

@visualize_bp.route('/visualize/correlation_heatmap', methods=['GET'])
def viz_correlation_heatmap():
    fig = plt.figure(figsize=(10, 8))
    plot_correlation_heatmap(df)
    return jsonify({'image': fig_to_base64(fig)})

@visualize_bp.route('/visualize/gender_cancer_counts', methods=['GET'])
def viz_gender_cancer_counts():
    fig = plt.figure(figsize=(8, 6))
    plot_gender_cancer_counts(df)
    return jsonify({'image': fig_to_base64(fig)})

@visualize_bp.route('/visualize/age_group_stacked_bar', methods=['GET'])
def viz_age_group_stacked_bar():
    fig = plt.figure(figsize=(12, 6))
    plot_age_group_stacked_bar(df)
    return jsonify({'image': fig_to_base64(fig)})

@visualize_bp.route('/visualize/smoking_boxplot', methods=['GET'])
def viz_smoking_boxplot():
    fig = plt.figure(figsize=(6, 4))
    plot_smoking_boxplot(df)
    return jsonify({'image': fig_to_base64(fig)})
