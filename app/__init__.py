from flask import Flask
from flask_bootstrap import Bootstrap
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.moment import Moment
import os

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] =\
 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SECRET_KEY'] = 'something super secret!'
app.config['DEBUG'] = True

db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
bootstrap = Bootstrap(app)
login_manager = LoginManager(app)
moment = Moment(app)

login_manager.session_protection = 'strong'
login_manager.login_view = 'login'
manager.add_command('db', MigrateCommand)

from app import views, models
