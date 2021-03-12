from ..main import task_queue, db
from ..models.data import *
from flask_sqlalchemy import SQLAlchemy
import xml.etree.ElementTree as ET
import requests
import json
from celery.result import AsyncResult


@task_queue.task
def show_trials():
    all_trials = db.session.query(Trials).all()
    return all_trials

# return all_data
@task_queue.task
def retrieve_trial_data(nct):
    all_data = db.session.query(Data).filter(Data.datum_belongs_to_trial == nct).all()
    return all_data

@task_queue.task
def retrieve_fields_from_db():
    all_data = db.session.query(Fields).all()
    return all_data

@task_queue.task
def write_field_to_db(response_object):
    field_name = response_object['field_name']
    field_note = response_object['field_note']
    field_meta = response_object['field_meta']
    new_field = Fields(field_meta,field_name,field_note, 'user created')
    db.session.add(new_field)
    db.session.commit()

@task_queue.task
def write_datapoint_to_db(response_object):

    # datum_value, datum_belongs_to_field, datum_belongs_to_trial, datum_note, datum_source
    # {'columnId': 'a6314a06-611f-4d1e-8721-a55bcd5c76c1', 'rowId': 'NCT03371992', 'cell': 'Other: Evaluation of Response by RECIST'}

    datum_value = response_object['cell']
    datum_belongs_to_field = response_object['columnId']
    datum_belongs_to_trial = response_object['rowId']
    if db.session.query(Data).filter(Data.datum_belongs_to_trial == datum_belongs_to_trial).filter(Data.datum_belongs_to_field == datum_belongs_to_field).filter(Data.datum_value == datum_value).count() == 0:
        new_datapoint = Data(datum_value, datum_belongs_to_field, datum_belongs_to_trial,'placeholder note','internal analysis')
        db.session.add(new_datapoint)
        db.session.commit()


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
    
    response = fetch_trial_document.delay(url)

    root = ET.fromstring(response.content)
    nct_from_response = root.find(".//Field[@Name='NCTId']").text
    datapoints = root.findall('.//Field')

    add_trial_to_trial_table.delay(nct_from_response)

    for datapoint in datapoints:
        field_uid_from_db = get_field_uid_from_db.delay(datapoint)
        datapoint.set('Field ID', field_uid_from_db)

    
    for datapoint in datapoints:
        add_datapoint_to_db.delay(datapoint,nct_from_response, url)
    
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



@task_queue.task
def process_csv(csv, mapping):

    return {csv, mapping}