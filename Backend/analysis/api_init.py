from flask import Blueprint, jsonify, current_app
import logging

def create_analysis_bp():
    """创建分析蓝图"""
    analysis_bp = Blueprint('analysis_bp', __name__)
    
    # 引入各个图表的API处理函数
    from .age_distribution import get_age_distribution
    from .gender_cancer import get_gender_cancer_stats
    from .correlation_matrix import get_correlation_matrix
    from .age_group_stats import get_age_group_stats
    from .smoking_stats import get_smoking_stats
    from .patient_counts import get_patient_counts
    
    @analysis_bp.route('/age-distribution', methods=['GET'])
    def age_distribution_api():
        """年龄分布图表API"""
        try:
            result = get_age_distribution()
            return jsonify(result)
        except Exception as e:
            logging.error(f"Error in age_distribution_api: {str(e)}")
            return jsonify({"error": str(e)}), 500
    
    @analysis_bp.route('/gender-cancer', methods=['GET'])
    def gender_cancer_api():
        """性别与肺癌关系图表API"""
        try:
            result = get_gender_cancer_stats()
            return jsonify(result)
        except Exception as e:
            logging.error(f"Error in gender_cancer_api: {str(e)}")
            return jsonify({"error": str(e)}), 500
    
    @analysis_bp.route('/correlation-matrix', methods=['GET'])
    def correlation_matrix_api():
        """相关性矩阵图表API"""
        try:
            result = get_correlation_matrix()
            return jsonify(result)
        except Exception as e:
            logging.error(f"Error in correlation_matrix_api: {str(e)}")
            return jsonify({"error": str(e)}), 500
    
    @analysis_bp.route('/age-group-stats', methods=['GET'])
    def age_group_stats_api():
        """年龄组统计图表API"""
        try:
            result = get_age_group_stats()
            return jsonify(result)
        except Exception as e:
            logging.error(f"Error in age_group_stats_api: {str(e)}")
            return jsonify({"error": str(e)}), 500
    
    @analysis_bp.route('/smoking-stats', methods=['GET'])
    def smoking_stats_api():
        """吸烟与年龄图表API"""
        try:
            result = get_smoking_stats()
            return jsonify(result)
        except Exception as e:
            logging.error(f"Error in smoking_stats_api: {str(e)}")
            return jsonify({"error": str(e)}), 500
    
    @analysis_bp.route('/patient-counts', methods=['GET'])
    def patient_counts_api():
        """患者数量统计图表API"""
        try:
            result = get_patient_counts()
            return jsonify(result)
        except Exception as e:
            logging.error(f"Error in patient_counts_api: {str(e)}")
            return jsonify({"error": str(e)}), 500
    
    return analysis_bp 