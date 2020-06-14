from flask import Flask, url_for
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
import db_actions

database = "sqlite:///database/spending.db"

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = database
app.config['SECRET_KEY'] = "WooWeeWhateverKey"
db = SQLAlchemy(app)



@app.route("/")
def home():
    return render_template('index.html')
    
@app.route("/configure")
def configure():
	users = [ "Charlie", "Abby", "Caylee" ]
	return render_template('configure.html', users=users)
	
@app.route("/data")
def showData():
    return render_template('data.html')

if __name__=="__main__":
	app.run(debug=True)
