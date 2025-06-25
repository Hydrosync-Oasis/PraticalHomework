from flask import Blueprint, jsonify
from ..spark_analysis import get_scatter_age_charges_smoker

scatter_age_api = Blueprint('scatter_age_api', __name__)

@scatter_age_api.route('/', methods=['GET'])
def scatter_age():
    data = get_scatter_age_charges_smoker()
    return jsonify(data)
