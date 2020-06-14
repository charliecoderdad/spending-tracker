from tracker_app import app
from flask import render_template, url_for

print("Hey CHARLIE HART I GOT HERE")

@app.route("/")
def home():
	print("IN THE HOME ROUTE HOMEY")
	return render_template('index.html')
    
@app.route("/configure")
def configure():
	users = [ "Charlie", "Abby", "Caylee" ]
	return render_template('configure.html', users=users)
	
@app.route("/data")
def showData():
    return render_template('data.html')
