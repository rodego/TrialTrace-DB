from ..main import task_queue, db
from flask_sqlalchemy import SQLAlchemy
import requests
import json


# @task_queue.task
# def process_trial(trial_id):


@task_queue.task(bind=True)
def get_all_trial_fields(self):
    url = 'https://clinicaltrials.gov/api/info/study_fields_list?fmt=JSON'
    response = requests.get(url)
    response_dict = response.json()

    api_version = response_dict['APIVrs']
    fields = response_dict['Fields']
    for field in fields:
        data = Fields(field, api_version, url, "auto", None)
        db.session.add(data)
        db.session.commit()
    return 201


