from flask import Flask
#from flask_bootstrap import Bootstrap
from flask_material import Material
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.moment import Moment
import os

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] =\
 os.environment.get('SQLALCHEMY_DATABASE_URI')
app.config['SECRET_KEY'] = os.environment.get('SECRET_KEY')
app.config['DEBUG'] = True

db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
Material(app)
login_manager = LoginManager(app)
moment = Moment(app)

login_manager.session_protection = 'strong'
login_manager.login_view = 'login'
manager.add_command('db', MigrateCommand)

from app import views, models
