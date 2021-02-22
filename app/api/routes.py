from flask import Blueprint, jsonify
from flask_restful import Resource, Api



api = Blueprint('api', __name__, url_prefix='/api')
rest = Api(api)

class Example(Resource):
  def get(self):
    return {'data':[
      {
        'best': 'friend',
        'op': 'buddy',
      },
      {
        'best': 'friend',
        'gringo': 'buddy',
      },

      ]}



rest.add_resource(Example, '/')
