import os 
import requests


from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv

from oauthlib.oauth2 import WebApplicationClient


load_dotenv()


app = Flask(__name__)


app.secret_key = os.environ.get('SECRET_KEY')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/googlelogin.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'primary'

oauth = WebApplicationClient(os.environ.get('GOOGLE_OAUTH2_CLIENT_ID'))


from googlelogin import routes