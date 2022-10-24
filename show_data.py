from flask import Blueprint, render_template, request, abort, jsonify, current_app
from jinja2 import TemplateNotFound

from .authentication import authentication_required

import csv

show_data = Blueprint('show_data', 
                        __name__, 
                        template_folder='templates/show_data', 
                        static_folder='static')

def read_csv(file):
    rows = []
    with open(file, 'r') as file:
        my_reader = csv.reader(file, delimiter=',')
        for row in my_reader:
            rows.append(row)
    return rows


@show_data.route('/data', methods=['GET'])
@authentication_required
def data():
    csv_file = 'static/data/world_population.csv'
    rows = read_csv(csv_file)
    context = {}
    context['rows'] = rows

    try:
        return render_template('data.html', context=context)
    except TemplateNotFound as e:
        current_app.logger.error("TemplateNotFound")
        abort(404)