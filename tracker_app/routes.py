from tracker_app import app, db
from flask import render_template, url_for, flash, redirect
from tracker_app import forms, displayData, analyzeData
from tracker_app.models import User, Category, Expense, Metadata
from sqlalchemy import and_
import datetime, calendar

@app.route("/analysis/", methods=["GET", "POST"])
@app.route("/analysis/<year>", methods=["GET", "POST"])
def yearlyAnalysis(year='none', month='none'):
	if (year == "none"):
		year = datetime.datetime.today().year
		
	analysisForm = forms.YearlyAnalysisConfigureForm()
	analysisForm.year.choices = [r.year for r in Metadata.query.with_entities(Metadata.year).distinct().order_by(Metadata.year.desc()).all()]
	
	analyze = analyzeData.AnalyzeData(year)
	stats = analyze.getAnalysisStats()
	return render_template('yearlyAnalysis.html', analysisForm=analysisForm, stats=stats, yearStr=year)

@app.route("/showData/", methods=["GET", "POST"])
@app.route("/showData/<year>/<month>", methods=["GET", "POST"])
def showData(year='none', month='none'):
		
	if (year == "none" or year =="deleteExpense"):
		year = datetime.datetime.today().year
		month = datetime.datetime.today().month

	# Get the dynamice HTML content for the page
	display = displayData.DisplayData(year, month)
	#myHtml = display.getPage()
	expenseTable = display.getExpenseTable()
	analyzeTable = display.getAnalyzeTable()
	stats = display.getExpenseStats()
	#monthStr = display.start_date.strftime("%B, %Y")	
	monthStr = str(calendar.month_name[int(month)]) + ", " + str(year)

	expenseConfigForm = forms.ExpenseConfigureForm()
	expenseConfigForm.year.choices = [r.year for r in Metadata.query.with_entities(Metadata.year).distinct().order_by(Metadata.year.desc()).all()]
	if expenseConfigForm.validate_on_submit():
		print("Got here")
		return redirect(url_for('showData', year=expenseConfigForm.year.data, month=expenseConfigForm.month.data))
		
	return render_template('monthlyData.html', analyzeTable=analyzeTable, expenseTable=expenseTable, stats=stats, 
		monthStr=monthStr, expenseConfigForm=expenseConfigForm)

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
