from flask import jsonify, render_template, redirect, request, Blueprint
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
                write_datapoints_to_db(trial)
            
            return redirect(request.referrer)
        else:
            return redirect(request.referrer)        
    @expose('/upload', methods=('GET', 'POST'))
    def upload(self):
        if request.method == 'POST' and request.files.get('file'):
            response = request.files.get('file')
            df = pd.read_csv(response)
            handoff = df.to_json()
            columns_to_import = df.columns
            #TODO filter for fields that are important
            data_fields = retrieve_fields_from_db()
            trial_fields = Trials.__table__.columns.keys()
            x = store_df_in_queue.delay(handoff)

            # print(trial_fields)
            return self.render('admin/index.html', task=x.task_id, options=columns_to_import, data_fields=data_fields, trial_fields=trial_fields)
        else:
            return redirect(request.referrer)


    @expose('/import', methods=('GET', 'POST'))
    def import_fields(self):
         if request.method == 'POST':
            # response = retrieve_df_from_queue()
            # df = pd.read_json(response)
            # print(df)
            x = request.form.get('task')
            sheet_object = retrieve_df_from_queue(x)
            pd.read_json(sheet_object)
            to_include = request.form.getlist('include')
            
            for field in to_include:
                mapped_to_field = request.form.get(field)
                print(mapped_to_field)
            # data = request.form.getlist('fields')
            # print( to_include)
            # pass
            return self.render('admin/index.html')
        






class ModelViewWithKeys(ModelView):
    column_display_pk = True

class ModelViewWithEditsInline(ModelView):
    column_editable_list = ('view', 'field', 'field_order')
    # edit_modal = True
    # create_modal = True

admin = Admin(index_view=MyHomeView(url='/'), template_mode='bootstrap3')

admin.add_view(ModelViewWithKeys(Trials, db.session))
admin.add_view(ModelView(Data, db.session))
admin.add_view(ModelView(Fields, db.session))
admin.add_view(ModelView(Views, db.session))
admin.add_view(ModelViewWithEditsInline(FieldsViews, db.session))

