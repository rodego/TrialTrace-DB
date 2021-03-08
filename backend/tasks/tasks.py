from ..main import task_queue, db
from ..models.data import *
from flask_sqlalchemy import SQLAlchemy
import xml.etree.ElementTree as ET
import requests
import json


@task_queue.task
def show_trials():
    all_trials = db.session.query(Trials).all()
    return all_trials

@task_queue.task
def retrieve_trial_data(nct):
    all_data = db.session.query(Data).filter(Data.datum_belongs_to_trial == nct).all()
    return all_data

@task_queue.task
def retrieve_fields_from_db():
    all_data = db.session.query(Fields).all()
    return all_data

@task_queue.task
def add_field_to_db(response_object):
    field_name = response_object['field_name']
    field_note = response_object['field_note']
    field_meta = response_object['field_meta']
    new_field = Fields(field_meta,field_name,field_note, 'user created')
    db.session.add(new_field)
    db.session.commit()
    # return all_data

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
def fetch_trial_document(self, url):
    
    response = requests.get(url)

    return response


@task_queue.task(bind=True)
def write_datapoints_to_db(self, nct):

    base_url = 'https://clinicaltrials.gov/api/query'
    url = f'{base_url}/full_studies?expr={nct}&min_rnk=1&max_rnk=1&fmt=xml'    
    
    response = fetch_trial_document(url)

    root = ET.fromstring(response.content)
    nct_from_response = root.find(".//Field[@Name='NCTId']").text
    datapoints = root.findall('.//Field')

    add_trial_to_trial_table(nct_from_response)

    for datapoint in datapoints:
        field_uid_from_db = get_field_uid_from_db(datapoint)
        datapoint.set('Field ID', field_uid_from_db)

    
    for datapoint in datapoints:
        add_datapoint_to_db(datapoint,nct_from_response, url)
    
    return 201


@task_queue.task(bind=True)
def add_trial_to_trial_table(self, nct):
    
    if db.session.query(Trials).filter(Trials.trial_id == nct).count() == 0:
        trial_to_insert = Trials(nct,None,None,None)
        db.session.add(trial_to_insert)
        db.session.commit()
    else:
        db.session.query(Trials).filter(Trials.trial_id == nct).update({})
        db.session.commit()
    return 201


######## helpers #######

@task_queue.task(bind=True)
def get_trial_data_from_db(self, nct):
    pass


@task_queue.task(bind=True)
def get_field_uid_from_db(self,datapoint_object):
    
    field_name_from_doc = datapoint_object.get('Name')
    #TODO add check for APIvrs
    field_uid_from_db = db.session.query(Fields.field_uid).filter(Fields.field_name == field_name_from_doc)
    return field_uid_from_db


@task_queue.task(bind=True)
def add_datapoint_to_db(self,datapoint_object, nct_from_response, url):
    
    # read datapoint text and field id (prev modified) from the object
    
    datum_value_to_db = datapoint_object.text
    field_uid_to_db = datapoint_object.get('Field ID')

    if db.session.query(Data).filter(Data.datum_belongs_to_trial == nct_from_response).filter(Data.datum_belongs_to_field == field_uid_to_db).filter(Data.datum_value == datum_value_to_db).count() == 0:

    # blindspot here is what if a value goes back to the same value as it was before. 
    # need some sort of time element here
    # also what if there are repeat values for a field

        data_to_insert = Data(datum_value_to_db,field_uid_to_db,nct_from_response,None,url)
        db.session.add(data_to_insert)
        db.session.commit()