from flask import Blueprint, jsonify, render_template, redirect, request
from flask_restful import Resource, Api
from ..tasks.tasks import *
import re
from .fields import common_fields
# from time import sleep



admin = Blueprint('admin', __name__, url_prefix='/admin', template_folder='.')
rest = Api(admin)


@admin.route('/')
def index():
    all_trials = show_trials()
    return render_template('admin.html', trials=all_trials)



class Trials(Resource):
    def post(self):
        trial_ids_raw = request.form['trial-list']
        if trial_ids_raw:
            trial_ids = re.findall(r'(NCT[0-9]+)', trial_ids_raw)
            for trial in trial_ids:
                write_datapoints_to_db(trial)
            
            return redirect(request.referrer)
        else:
            return redirect(request.referrer)



rest.add_resource(Trials, '/trials')
