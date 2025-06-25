from flask import Blueprint, jsonify
from Backend.app.spark_analysis import get_scatter_bmi_charges

scatter_bmi_api = Blueprint('scatter_bmi_api', __name__)

@scatter_bmi_api.route('/', methods=['GET'])
def scatter_bmi():
    data = get_scatter_bmi_charges()
    return jsonify(data)
