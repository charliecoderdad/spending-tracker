from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

#database = "sqlite:///spending.db"
database = "sqlite:///spending.db"

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = database
app.config['SECRET_KEY'] = "WooWeeWhateverKey"
db = SQLAlchemy(app)

from tracker_app import routes
