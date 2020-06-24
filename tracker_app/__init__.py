from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import configparser

config = configparser.ConfigParser()
config.read('./config/tracker_app.conf')

database = config['Default']['Database_URI']

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = database
app.config['SECRET_KEY'] = "WooWeeWhateverKey"
db = SQLAlchemy(app)
from tracker_app.models import Expense, Metadata, User, Category
db.create_all()
db.session.commit()

from tracker_app import routes
