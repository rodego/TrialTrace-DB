from ..main import task_queue, db
from ..models.data import Fields
from flask_sqlalchemy import SQLAlchemy
import requests
import json


# @task_queue.task
# def process_trial(trial_id):

# get all the possible fields from clinicaltrials.gov

@task_queue.task(bind=True)
def get_all_trial_fields(self):
    url = 'https://clinicaltrials.gov/api/info/study_fields_list?fmt=JSON'
    response = requests.get(url)
    response_dict = response.json()
    response_dict_unfurl = response_dict['StudyFields']
    api_version = response_dict_unfurl['APIVrs']
    fields = response_dict_unfurl['Fields']
    for field in fields:
        data = Fields(api_version,field, None, url)
        db.session.add(data)
        db.session.commit()
    return 201



@task_queue.task(bind=True)
def get_data_for_trial(self, nct, fields=[]):
    
    base_url = 'https://clinicaltrials.gov/api/query'

    # if fields == []:
    #     url = f'{base_url}/full_studies?expr={nct}&min_rnk=1&max_rnk=1&fmt=json'
    # else: 
    field_concat = '%2C'.join(fields)
    url = f'{base_url}/study_fields?expr={nct}&fields=NCTId{field_concat}&min_rnk=1&max_rnk=1&fmt=json'
    
    response = requests.get(url)
    response_dict = response.json()
    return response_dict
