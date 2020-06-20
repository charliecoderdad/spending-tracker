from tracker_app import app, db
from flask import render_template, url_for, flash, redirect
from tracker_app import forms, displayData
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
		formattedAmount = "{:.2f}".format(newExpenseForm.amount.data)
		print(f"Charlie: Formatted amount {formattedAmount}")
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
	return render_template('configure.html', users=User.query.order_by(User.username).all(), newUserForm=newUserForm,
				newCategoryForm=newCategoryForm, categories=Category.query.order_by(Category.expenseCategory).all())

@app.route("/deleteCategory/<categoryId>", methods=["GET","POST"])
def deleteCategory(categoryId):
	deletedCategory = Category.query.filter(Category.categoryId == categoryId).first().expenseCategory
	Category.query.filter(Category.categoryId == categoryId).delete()
	db.session.commit()
	flash(f"Category '{deletedCategory}' has been successfully removed", "success")
	return redirect(url_for('configure'))
	
@app.route("/deleteUser/<userId>", methods=["GET","POST"])
def deleteUser(userId):
	deletedUser = User.query.filter(User.userId == userId).first().username
	User.query.filter(User.userId == userId).delete()
	db.session.commit()
	flash(f"User '{deletedUser}' has been successfully removed", "success")
	return redirect(url_for('configure'))
	
@app.route("/deleteExpense/<expenseId>", methods=["GET","POST"])
def deleteExpense(expenseId):
	Expense.query.filter(Expense.expenseId == expenseId).delete()
	db.session.commit()
	flash(f"Expense has been successfully removed", "success")
	return redirect(url_for('showData'))
	
@app.route("/showData")
def showData():
	expenseTable = displayData.getExpenseTable(Expense=Expense, Category=Category, User=User)
	return render_template('data.html', expenseTable=expenseTable)
