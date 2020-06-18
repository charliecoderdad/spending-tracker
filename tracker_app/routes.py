from tracker_app import app, db
from flask import render_template, url_for, flash, redirect
from tracker_app import forms
from tracker_app.models import User, Category

@app.route("/", methods=["GET","POST"])
def home():
	print("CHARLIE IS GETTING NEW EXPENSE FORM SON")
	newExpenseForm = forms.NewExpenseForm()
	cats = Category.query.all()
	catList = []
	for cat in cats:
		catList.append(cat.expenseCategory)
	newExpenseForm.category.choices = catList
	
	return render_template('index.html', newExpenseForm=newExpenseForm)
    
@app.route("/configure", methods=["GET","POST"])
def configure():
	newUserForm = forms.NewUserForm()
	newCategoryForm = forms.NewCategoryForm()
	if newUserForm.validate_on_submit():
		user = User(username=newUserForm.username.data)
		db.session.add(user)
		db.session.commit()
		flash(f"User '{user.username}' has been successfully added", "success")
		return redirect(url_for('configure'))
	if newCategoryForm.validate_on_submit():
		cat = Category(expenseCategory=newCategoryForm.category.data)
		db.session.add(cat)
		db.session.commit()
		flash(f"User '{cat.expenseCategory}' has been successfully added", "success")
		return redirect(url_for('configure'))
	return render_template('configure.html', users=User.query.all(), newUserForm=newUserForm,
				newCategoryForm=newCategoryForm, categories=Category.query.all())

@app.route("/deleteCategory/<categoryId>", methods=["GET","POST"])
def deleteCategory(categoryId):
	deletedCategory = Category.query.filter(Category.categoryId == categoryId).first().expenseCategory
	Category.query.filter(Category.categoryId == categoryId).delete()
	db.session.commit()
	flash(f"Category '{deletedCategory}' has been successfully removed", "success")
	return redirect(url_for('configure'))
	
@app.route("/deleteUser/<userid>", methods=["GET","POST"])
def deleteUser(userid):
	deletedUser = User.query.filter(User.userId == userid).first().username
	User.query.filter(User.userId == userid).delete()
	db.session.commit()
	flash(f"User '{deletedUser}' has been successfully removed", "success")
	return redirect(url_for('configure'))
	
@app.route("/showData")
def showData():
    return render_template('data.html')
