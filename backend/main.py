
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, current_user, login_user, logout_user, login_required, current_user
from flask_cors import CORS
from celery import Celery
import re
import os





# instantiate components

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
cors = CORS()


# environment

ENV = os.uname().sysname


if ENV == os.getenv("SYSTEM"):
    masterconfig = {'debug': False, 'db': os.getenv("DATABASE_URL"), 'task-broker': os.getenv("ELERY_BROKER")}

else:
    masterconfig = {'debug': True, 'db': os.getenv("DEV_DATABASE_ADDRESS"), 'task-broker': os.getenv("DEV_CELERY_BROKER")}


task_queue = Celery(__name__, broker=masterconfig['task-broker'], backend=masterconfig['task-broker'])



def create_app():
    app = Flask(__name__)
    app.secret_key = os.getenv("SECRET_KEY")
    app.debug = masterconfig['debug']
    app.config['SQLALCHEMY_DATABASE_URI'] = masterconfig['db']
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


    
    db.init_app(app)
    migrate.init_app(app,db)

    # from backend.models.data import Trials, Data, Fields
    # from backend.models.ux import Views

    import backend.models.users

    from backend.api.routes import api
    from backend.admin.routes import admin
    
    app.register_blueprint(api)
    # app.register_blueprint(adminblu)

    admin.init_app(app)
    login.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": "*"}})

    task_queue.conf.update(app.config)
    

    # @app.route('/')
    # def index():
    #     return render_template('index.html')
    
    @login.user_loader
    def load_user(user_id):
        return Users.query.get(user_id)

    
    

    return app
        



