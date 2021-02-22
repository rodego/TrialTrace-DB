
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, current_user, login_user, logout_user, login_required, current_user
from flask_cors import CORS
import re
import os

from .api.routes import api
from .admin.routes import admin



# instantiate components

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
cors = CORS()

# environment

ENV = os.uname().sysname


if ENV == os.getenv("SYSTEM"):
    masterconfig = {'debug': False, 'db': os.getenv("DATABASE_URL")}

else:
    masterconfig = {'debug': True, 'db': os.getenv("DEV_DATABASE_ADDRESS")}




def create_app():
    app = Flask(__name__)
    app.secret_key = os.getenv("SECRET_KEY")
    app.debug = masterconfig['debug']
    app.config['SQLALCHEMY_DATABASE_URI'] = masterconfig['db']
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


    
    db.init_app(app)
    migrate.init_app(app,db)
    from app.models.data import Data
    from app.models.users import Users
    
    app.register_blueprint(api)
    app.register_blueprint(admin)


    login.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": "*"}})


    

    # @app.route('/')
    # def index():
    #     return render_template('index.html')
    
    @login.user_loader
    def load_user(user_id):
        return Users.query.get(user_id)

        
    return app
        



