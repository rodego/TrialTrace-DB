from flask import jsonify, render_template, redirect, request, Blueprint, session
from flask_restful import Resource, Api
from ..tasks.tasks import *
import re
from .fields import common_fields
from flask_admin import Admin, BaseView, expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView

from backend.models.data import Trials, Data, Fields
from backend.models.ux import Views, FieldsViews
import pandas as pd



class MyHomeView(AdminIndexView):
    @expose('/')
    def index(self):
        # self.blueprint = Blueprint(self.endpoint, __name__,template_folder=op.join('admin', self.admin.template_mode))
        # arg1 = 'Hello'
        return self.render('admin/index.html')
    @expose('/add', methods=('GET', 'POST'))
    def add(self):
        trial_ids_raw = request.form['trial-list']
        if trial_ids_raw:
            trial_ids = re.findall(r'(NCT[0-9]+)', trial_ids_raw)
            for trial in trial_ids:
                write_datapoints_to_db.delay(trial)
            
            return redirect(request.referrer)
        else:
            return redirect(request.referrer)        
    @expose('/upload', methods=('GET', 'POST'))
    def upload(self):
        if request.method == 'POST' and request.files.get('file'):
            response = request.files.get('file')
            df = pd.read_csv(response)
            columns_to_import = df.columns
            
            #TODO filter for fields that are important

            def high_value(field):
                if field.field_include == True:
                    return True
                else: False

            db_fields = retrieve_fields_from_db()

            data_fields = list(filter(high_value,db_fields))
            trial_fields = Trials.__table__.columns.keys()
            
            # store as backend session to be recalled later
            handoff = df.to_json()
            session['dataframe'] = handoff

            return self.render('admin/index.html', 
                                options=columns_to_import, 
                                data_fields=data_fields, 
                                trial_fields=trial_fields,
                                )
        else:
            return redirect(request.referrer)


    @expose('/import', methods=('GET', 'POST'))
    def import_fields(self):
         if request.method == 'POST':
            sheet_object = session.get('dataframe')
            # sheet = pd.read_json(sheet_object)


            to_include = request.form.getlist('include')



            # to_map = request.form.getlist[(include']
            # to_add = request.form.getlist['include']

            mapping = {'to_include': to_include}

            print(mapping)

            process_csv.delay(sheet_object, mapping)
            

            # for x in (x for x in xyz if x not in a)
            for field in to_include:
                mapped_to_field = request.form.get(field)
                print(mapped_to_field)

            return self.render('admin/index.html', message=to_include)
        






class ModelViewWithKeys(ModelView):
    column_display_pk = True


#TODO make this into a single class that accepts kwargs to change inline editable columns
class FieldViewsEdit(ModelView):
    column_editable_list = ['field_order', 'field', 'view']
class FieldEdit(ModelView):
    column_editable_list = ['field_include']



admin = Admin(index_view=MyHomeView(url='/'), template_mode='bootstrap3')

admin.add_view(ModelViewWithKeys(Trials, db.session))
admin.add_view(ModelView(Data, db.session))
admin.add_view(FieldEdit(Fields, db.session ))
admin.add_view(ModelView(Views, db.session))
admin.add_view(FieldViewsEdit(FieldsViews, db.session))

