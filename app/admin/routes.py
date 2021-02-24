from flask import Blueprint, jsonify, render_template, redirect
from flask_restful import Resource, Api
from ..tasks.tasks import get_all_trial_fields
# from time import sleep



admin = Blueprint('admin', __name__, url_prefix='/admin', template_folder='.')
rest = Api(admin)


# @admin.route('/')
# def index():
#     return render_template('admin.html')


class Trials(Resource):
    def get(self):
    # if request.form['trial-list']:
        # trial_ids_raw = request.form['trial-list']
        # trial_ids = re.findall(r'(NCT[0-9]+)', trial_ids_raw)
        # for trial in trial_ids:
        get_all_trial_fields
        # response = fields.get()

        return {'message': 'data added'}, 201
    # else:
    #     return {'message': 'no data added'}, 400



rest.add_resource(Trials, '/')
