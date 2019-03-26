from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, models

path_object = os.path.join('app', 'saved_states', 'state_test.pkl')
path_image = os.path.join('app', 'static', 'saved_state_images', 'cube_state_test.svg')
if os.path.exists(path_object):
    os.remove(path_object)
    os.remove(path_image)