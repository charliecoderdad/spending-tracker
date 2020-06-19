from tracker_app import app, db
from flask import render_template, url_for, flash, redirect
from tracker_app import forms
from tracker_app.models import User, Category, Expense
from datetime import date

@app.route("/", methods=["GET","POST"])
def home():
	newExpenseForm = forms.NewExpenseForm()
	sortedCategoriesList = [(c.categoryId, c.expenseCategory) for c in Category.query.all()]
	sortedCategoriesList.sort(key = lambda x: x[1])
	newExpenseForm.expenseCategory.choices = sortedCategoriesList
	newExpenseForm.spender.choices = [(u.userId, u.username) for u in User.query.all()]
	if newExpenseForm.validate_on_submit():			
		print(f"CHARLIE: Date {newExpenseForm.date.data}")
		print(f"CHARLIE: Category {newExpenseForm.expenseCategory.data}")
		print(f"CHARLIE: Spender {newExpenseForm.spender.data}")
		print(f"CHARLIE: Amount {newExpenseForm.amount.data}")
		print(f"CHARLIE: Description {newExpenseForm.description.data}")
		expense = Expense(date=newExpenseForm.date.data, categoryId=newExpenseForm.expenseCategory.data,
						spenderId=newExpenseForm.spender.data, amount=newExpenseForm.amount.data, description=newExpenseForm.description.data)
		db.session.add(expense)
		db.session.commit()
		flash(f"Created a new expense record", "info")
		return redirect(url_for('home'))
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
		cat = Category(expenseCategory=newCategoryForm.category.data, discretionary=newCategoryForm.discretionary.data)
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
    return render_template('data.html', expenses=Expense.query.all(), User=User, Category=Category)
