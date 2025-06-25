from flask import Blueprint, jsonify
from ..spark_analysis import get_correlation_data

correlation_api = Blueprint('correlation_api', __name__)

@correlation_api.route('/', methods=['GET'])
def correlation():
    data = get_correlation_data()
    return jsonify(data)
