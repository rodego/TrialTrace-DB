from flask import Blueprint, jsonify, render_template, request
from flask_restful import Resource, Api


admin = Blueprint('admin', __name__, url_prefix='/admin', template_folder='.')
rest = Api(admin)


@admin.route('/')
def index():
    return render_template('admin.html')


class Trials(Resource):
    def post(self):
        if request.form['trial-list']:
            trial_ids_raw = request.form['trial-list']
            trial_ids = re.findall(r'(NCT[0-9]+)', trial_ids_raw)
        return 201


rest.add_resource(Trials, '/trials/mutate')
