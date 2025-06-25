from flask import Blueprint, jsonify
from ..spark_analysis import get_age_histogram

age_hist_api = Blueprint('age_hist_api', __name__)

@age_hist_api.route('/', methods=['GET'])
def age_hist():
    data = get_age_histogram()
    return jsonify(data)
