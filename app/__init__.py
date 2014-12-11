from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import os
from flask.ext.login import LoginManager
#from config import basedir

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

login_manager=LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

from app import views, models