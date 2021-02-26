from flask import Blueprint, jsonify
from flask_restful import Resource, Api
from ..tasks.tasks import *
import json



api = Blueprint('api', __name__, url_prefix='/api')
rest = Api(api)

class Cell():
  def __init__(self, field, value):
    self.field = field
    self.value = value

class Example(Resource):
  def get(self):

    data = []
    trials = show_trials()
    for trial in trials:
      datapoints = show_trial_data(trial.trial_id)
      row = {}
      for datapoint in datapoints:
        value = str(datapoint.datum_value)
        field = str(datapoint.datum_belongs_to_field)
        cell =  {field : value}
        row.update(cell)
      data.append(row)
    print(data)
    return {'data': data}

rest.add_resource(Example, '/')
