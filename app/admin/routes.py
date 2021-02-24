from flask import Blueprint, jsonify, render_template, redirect, request
from flask_restful import Resource, Api
from ..tasks.tasks import get_data_for_trial
import re
from .fields import common_fields
# from time import sleep



admin = Blueprint('admin', __name__, url_prefix='/admin', template_folder='.')
rest = Api(admin)


@admin.route('/')
def index():
    return render_template('admin.html')



class Trials(Resource):
    def post(self):
        trial_ids_raw = request.form['trial-list']
        if trial_ids_raw:
            trial_ids = re.findall(r'(NCT[0-9]+)', trial_ids_raw)
            results = []
            for trial in trial_ids:
                # print(fields)
                response = get_data_for_trial(trial, common_fields)
                results.append(response)
            return  results , 201
        else:
            return {'message': 'no data added'}, 400



rest.add_resource(Trials, '/trials')
