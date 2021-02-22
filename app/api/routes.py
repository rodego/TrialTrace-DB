from flask import Blueprint, jsonify


api = Blueprint('api', __name__, url_prefix='/api')


@api.route('/')
def get():
    return      jsonify(
        { 'data' : [{
         'col1': 'Hello',
         'col2': 'World',
       },
       {
         'col1': 'react-table',
         'col2': 'rocks',
       },
       {
         'col1': 'whatever',
         'col2': 'you want',
       },
       {
         'col1': 'whatever',
         'col2': 'you want',
       },
       {
         'col1': 'hey',
         'col2': 'you',
       }
       ,
       {
         'col1': 'i love',
         'col2': 'fra',
       }
       ]
       }), 200