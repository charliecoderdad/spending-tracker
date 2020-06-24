from tracker_app import app, db
from flask import render_template, url_for, flash, redirect
from tracker_app import forms, monthInfo, yearInfo, categoryTable
from tracker_app.models import User, Category, Expense, Metadata
from sqlalchemy import and_
import datetime, calendar

@app.route("/yearlyAnalysis/", methods=["GET", "POST"])
@app.route("/yearlyAnalysis/<year>/<spender>", methods=["GET", "POST"])
def yearlyAnalysis(year=None, spender=None):
	if (year is None):
		year = datetime.datetime.today().year
		
	yearlyForm = forms.YearlyAnalysisConfigureForm()
	yearlyForm.year.choices = [r.year for r in Metadata.query.with_entities(Metadata.year).distinct().order_by(Metadata.year.desc()).all()]
	spenderChoices = [u.username for u in db.session.query(User.username).all()]
	spenderChoices.append("All")
	yearlyForm.spender.choices = spenderChoices
	
	catTable = categoryTable.CategoryTable(year, spender=spender)
	categoryAnalysisTable = catTable.getCategoryAnalysisTable()
	
	analysis = yearInfo.YearInfo(year, spender=spender)
	stats = analysis.getYearlyStats()
	breakdownByMonthAnalysisTable = analysis.breakdownByMonthAnalysisTable()
	if yearlyForm.validate_on_submit():
		return redirect(url_for('yearlyAnalysis', year=yearlyForm.year.data, spender=yearlyForm.spender.data))
	
	return render_template('yearlyAnalysis.html', yearlyForm=yearlyForm, stats=stats, yearStr=year,
			categoryAnalysisTable=categoryAnalysisTable, breakdownByMonthAnalysisTable=breakdownByMonthAnalysisTable, spender=spender)

@app.route("/monthlyAnalysis/", methods=["GET", "POST"])
@app.route("/monthlyAnalysis/<year>/<month>/<spender>", methods=["GET", "POST"])
def monthlyAnalysis(year=None, month=None, spender=None):
		
	if (year is None or year =="deleteExpense"):
		year = datetime.datetime.today().year
		month = datetime.datetime.today().month

	analysis = monthInfo.MonthInfo(year, month, spender)
	
	catTable = categoryTable.CategoryTable(year, month=month, spender=spender)
	categoryAnalysisTable = catTable.getCategoryAnalysisTable()
	
	expenseTable = analysis.getExpenseTable()
	stats = analysis.getMonthlyExpenseStats()
	monthStr = str(calendar.month_name[int(month)]) + ", " + str(year)

	monthlyForm = forms.ExpenseConfigureForm()
	monthlyForm.year.choices = [r.year for r in Metadata.query.with_entities(Metadata.year).distinct().order_by(Metadata.year.desc()).all()]
	spenderChoices = [u.username for u in db.session.query(User.username).all()]
	spenderChoices.append("All")	
	monthlyForm.spender.choices = spenderChoices
	
	if monthlyForm.validate_on_submit():
		return redirect(url_for('monthlyAnalysis', year=monthlyForm.year.data, month=monthlyForm.month.data,
				spender=monthlyForm.spender.data))
		
	return render_template('monthlyData.html', categoryAnalysisTable=categoryAnalysisTable, expenseTable=expenseTable, stats=stats, 
		monthStr=monthStr, monthlyForm=monthlyForm, spender=spender)

@app.route("/", methods=["GET","POST"])
def home():
	newExpenseForm = forms.NewExpenseForm()
	sortedCategoriesList = [(c.categoryId, c.expenseCategory) for c in Category.query.all()]
	sortedCategoriesList.sort(key = lambda x: x[1])
	newExpenseForm.expenseCategory.choices = sortedCategoriesList
	newExpenseForm.spender.choices = [(u.userId, u.username) for u in User.query.all()]
	if newExpenseForm.validate_on_submit():
		# add expense record to database
		formattedAmount = "{:.2f}".format(newExpenseForm.amount.data)
		expense = Expense(date=newExpenseForm.date.data, categoryId=newExpenseForm.expenseCategory.data,
						spenderId=newExpenseForm.spender.data, amount=newExpenseForm.amount.data, description=newExpenseForm.description.data)
		db.session.add(expense)
		db.session.commit()
		# add metadata about expense to database
		if (bool(Metadata.query.filter(and_(Metadata.year == int(newExpenseForm.date.data.year), Metadata.monthNum == int(newExpenseForm.date.data.month))).first()) == False):
			print("Did not find a metadata so I'm adding one")
			md = Metadata(year=expense.date.year, monthNum=expense.date.month, monthStr=expense.date.strftime('%B'))
			db.session.add(md)
			db.session.commit()
		else:
			print("Already found a metadata you chuckle head!!!")
			
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
	categoryExistsInRecord = bool(db.session.query(Expense).filter(Expense.categoryId == categoryId).first())
	deletedCategory = Category.query.filter(Category.categoryId == categoryId).first().expenseCategory
	
	if categoryExistsInRecord:
		flash(f"Error: '{deletedCategory}' is being used in one or more records", "danger")
	else:				
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
	return redirect(url_for('monthlyAnalysis'))
