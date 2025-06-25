from flask import Blueprint, jsonify
from Backend.app.spark_analysis import get_region_avg_charges

region_avg_api = Blueprint('region_avg_api', __name__)

@region_avg_api.route('/', methods=['GET'])
def region_avg():
    data = get_region_avg_charges()
    return jsonify(data)
