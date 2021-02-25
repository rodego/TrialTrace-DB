from ..main import task_queue, db
from ..models.data import *
from flask_sqlalchemy import SQLAlchemy
import xml.etree.ElementTree as ET
import requests
import json


# @task_queue.task
# def process_trial(trial_id):

# get all the possible fields from clinicaltrials.gov

@task_queue.task(bind=True)
def get_all_trial_fields(self):
    url = 'https://clinicaltrials.gov/api/info/study_fields_list?fmt=XML'
    response = requests.get(url)
    root = ET.fromstring(response.content)
    api_version = root.find('.//APIVrs').text
    fields = root.findall['.//Field/@Name']
    for field in fields:
        data = Fields(api_version,field.text, None, url)
        db.session.add(data)
        db.session.commit()
    return 201



@task_queue.task(bind=True)
def get_data_for_trial(self, nct):
    
    base_url = 'https://clinicaltrials.gov/api/query'
    url = f'{base_url}/full_studies?expr={nct}&min_rnk=1&max_rnk=1&fmt=xml'    
    response = requests.get(url)

    # return response

    root = ET.fromstring(response.content)
    nct_from_response = root.find(".//Field[@Name='NCTId']").text
    datapoints = root.findall('.//Field')

    add_trial_to_trial_table(nct_from_response)

    for datapoint in datapoints:
        field = datapoint.get('Name')
        #TODO add check for APIvrs
        field_uid_from_db = db.session.query(Fields.field_uid).filter(Fields.field_name == field)
        datapoint.set('Field ID', field_uid_from_db)

    
    for datapoint in datapoints:
        datum_value_to_db = datapoint.text
        field_uid_to_db = datapoint.get('Field ID')
        if db.session.query(Data).filter(Data.datum_belongs_to_trial == nct_from_response).filter(Data.datum_belongs_to_field == field_uid_to_db).filter(Data.datum_value == datum_value_to_db).count() == 0:

            # blindspot here is what if a value goes back to the same value as it was before. 
            # need some sort of time element here
            # also what if there are repeat values for a field

            data_to_insert = Data(datum_value_to_db,field_uid_to_db,nct_from_response,None,url)
            db.session.add(data_to_insert)
            db.session.commit()
    
    return 201


@task_queue.task(bind=True)
def add_trial_to_trial_table(self, nct):
    
    if db.session.query(Trials).filter(Trials.trial_id == nct).count() == 0:
        trial_to_insert = Trials(nct,None,None)
        db.session.add(trial_to_insert)
        db.session.commit()
    else:
        db.session.query(Trials).filter(Trials.trial_id == nct).update({})
        db.session.commit()
    return 201

