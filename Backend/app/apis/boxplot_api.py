from flask import Blueprint, jsonify
from app.spark_analysis import get_boxplot_data

boxplot_api = Blueprint('boxplot_api', __name__)

@boxplot_api.route('/', methods=['GET'])
def boxplot():
    data = get_boxplot_data()
    return jsonify(data)
