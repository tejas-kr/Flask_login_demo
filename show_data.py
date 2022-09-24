from flask import Blueprint, render_template, request, abort, jsonify, current_app
from jinja2 import TemplateNotFound

show_data = Blueprint('show_data', __name__, template_folder='templates/show_data')


@show_data.route('/data', methods=['GET'])
def data():
    try:
        return render_template('dadta.html')
    except TemplateNotFound as e:
        current_app.logger.error("TemplateNotFound")
        abort(404)