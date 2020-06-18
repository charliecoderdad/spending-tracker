from tracker_app import app, db
from flask import render_template, url_for, flash, redirect
from tracker_app import forms
from tracker_app.models import User

@app.route("/")
def home():
	return render_template('index.html')
    
@app.route("/configure", methods=["GET","POST"])
def configure():
	newUserForm = forms.NewUserForm()
	if newUserForm.validate_on_submit():
		user = User(username=newUserForm.username.data)
		db.session.add(user)
		db.session.commit()
		flash('User has been added', 'success')
		return redirect(url_for('configure'))
	return render_template('configure.html', users=User.query.all(), newUserForm=newUserForm)
	
@app.route("/deleteUser/<userid>", methods=["GET","POST"])
def deleteUser(userid):
	print(f"Charlie debug: User to delete {userid}")
	User.query.filter(User.id == userid).delete()
	db.session.commit()
	return redirect(url_for('configure'))
	
@app.route("/data")
def showData():
    return render_template('data.html')
