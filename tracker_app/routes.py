from tracker_app import app, db
from flask import render_template, url_for, flash, redirect, request, Markup
from tracker_app import forms, monthInfo, yearInfo, categoryTable, searchData
from tracker_app.models import User, Category, Expense
from sqlalchemy import and_, extract
import datetime, calendar

@app.route("/search", methods=["GET", "POST"])
@app.route("/search/<startDate>/<endDate>/<category>/<spender>/<descText>", methods=["GET", "POST"])
def search(startDate="nodata", endDate="nodata", category="nodata", spender="nodata", descText="nodata"):
	searchForm = forms.SearchForm()
	
	searcher = searchData.SearchData(startDate=startDate, endDate=endDate, expenseCategory=category, spender=spender, descText=descText)
	
	print(f"Request path: {request.path}")
	if request.path == ('/search'):
		expenseTable = Markup("<br><h3>Choose search options</h3>")
	else:
		expenseTable = searcher.getExpenseTable()
	
	if searchForm.validate_on_submit():
		formStartDateValue = "nodata" if searchForm.startDate.data is None else searchForm.startDate.data
		formEndDateValue = "nodata" if searchForm.endDate.data is None else searchForm.endDate.data
		formCategoryValue = "nodata" if searchForm.expenseCategory.data is "" else searchForm.expenseCategory.data
		formSpenderValue = "nodata" if searchForm.spender.data is "" else searchForm.spender.data
		formDescTextValue = "nodata" if searchForm.descText.data is "" else searchForm.descText.data
		return redirect(url_for('search', startDate=formStartDateValue, endDate=formEndDateValue, category=formCategoryValue,
				spender=formSpenderValue, descText=formDescTextValue))
	
	
	sortedCategoriesList = [c.expenseCategory for c in Category.query.all()]
	sortedCategoriesList.sort()
	sortedCategoriesList.append("")
	searchForm.expenseCategory.choices = sortedCategoriesList
	searchForm.expenseCategory.process_data("")
	
	spenderChoices = [u.username for u in User.query.all()]
	spenderChoices.append("")
	searchForm.spender.process_data("")
	searchForm.spender.choices = spenderChoices

	# Set form values (based on prior search should be sticky)
	if startDate != "nodata":
		searchForm.startDate.process_data(datetime.datetime.strptime(startDate, "%Y-%m-%d"))
	if endDate != "nodata":
		searchForm.endDate.process_data(datetime.datetime.strptime(endDate, "%Y-%m-%d"))
	if category != "nodata":
		searchForm.expenseCategory.process_data(category)
	if spender != "nodata":
		searchForm.spender.process_data(spender)
	if descText != "nodata":
		searchForm.descText.process_data(descText)
	# End setting sticky forms
	
	
	return render_template("search.html", searchForm=searchForm, expenseTable=expenseTable)

@app.route("/editExpense/<expenseId>", methods=["GET", "POST"])
def editExpense(expenseId=None):
	editExpenseForm = forms.EditExpenseForm()
	global editReferrer	
	if request.method == "GET":
		print("We've got a GET method")
		editReferrer = request.referrer
		print(f"Referrer found {editReferrer}")
	if editExpenseForm.validate_on_submit():		
		print(f"Referrer found inside POST {editReferrer}")
		newCategoryId = db.session.query(Category.categoryId).filter(Category.expenseCategory == editExpenseForm.expenseCategory.data).first()[0]
		newSpenderId = db.session.query(User.userId).filter(User.username == editExpenseForm.spender.data).first()[0]
		
		e = db.session.query(Expense).get(expenseId)
		e.date = editExpenseForm.date.data
		e.categoryId = newCategoryId
		e.spenderId = newSpenderId
		e.amount = editExpenseForm.amount.data
		e.description = editExpenseForm.description.data		
		db.session.commit()
		
		flash(f"Expense record '{expenseId}' has been successfully updated", "success")
		#return redirect(url_for('home'))
		return redirect(editReferrer)
	
	expense = Expense.query.get(expenseId)	
	
	# Set defaults of the form to be equal to what expense we are editing
	editExpenseForm.date.process_data(expense.date)	
	editExpenseForm.amount.process_data(expense.amount)	
	editExpenseForm.description.process_data(expense.description)	
	spenderChoices = [u.username for u in db.session.query(User.username).all()]
	spenderChoices.append("All")
	editExpenseForm.spender.choices = spenderChoices
	editExpenseForm.spender.process_data(expense.spender.username)
	
	sortedCategoriesList = [c.expenseCategory for c in Category.query.all()]
	sortedCategoriesList.sort()
	editExpenseForm.expenseCategory.choices = sortedCategoriesList
	
	editExpenseForm.expenseCategory.process_data(expense.myCategory.expenseCategory)
	# End of setting default value of form to expense we are about to change
	
	return render_template('editExpense.html', editExpenseForm=editExpenseForm, expenseId=expenseId)	

@app.route("/yearlyAnalysis/", methods=["GET", "POST"])
@app.route("/yearlyAnalysis/<year>/<spender>", methods=["GET", "POST"])
def yearlyAnalysis(year=None, spender=None):
	if (year is None):
		year = datetime.datetime.today().year
		
	yearlyForm = forms.YearlyAnalysisConfigureForm()
	if yearlyForm.validate_on_submit():
		return redirect(url_for('yearlyAnalysis', year=yearlyForm.year.data, spender=yearlyForm.spender.data))
		
	yearlyForm.year.choices = [y[0] for y in db.session.query(extract('year', Expense.date)).distinct().all()]
	yearlyForm.year.process_data(year)
	
	spenderChoices = [u.username for u in db.session.query(User.username).all()]
	spenderChoices.append("All")
	yearlyForm.spender.choices = spenderChoices
	if spender is None:
		yearlyForm.spender.process_data("All")
	else:
		yearlyForm.spender.process_data(spender)
	
	catTable = categoryTable.CategoryTable(year, spender=spender)
	categoryAnalysisTable = catTable.getCategoryAnalysisTable()
	
	analysis = yearInfo.YearInfo(year, spender=spender)
	stats = analysis.getYearlyStats()
	breakdownByMonthAnalysisTable = analysis.breakdownByMonthAnalysisTable()	
	
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

	monthlyForm = forms.MonthlyAnalysisConfigureForm()		
	if monthlyForm.validate_on_submit():
		convertedStringToIntMonth = datetime.datetime.strptime(monthlyForm.month.data, "%B").month
		return redirect(url_for('monthlyAnalysis', year=monthlyForm.year.data, month=convertedStringToIntMonth,
				spender=monthlyForm.spender.data))

	monthlyForm.year.choices = [y[0] for y in db.session.query(extract('year', Expense.date)).distinct().all()]	

	# Set these SelectField default values to be same as what just queried
	monthlyForm.year.process_data(year)
	monthlyForm.month.process_data(calendar.month_name[int(month)])
	
	#monthlyForm.month.choices = [calendar.month_name[m[0]] for m in db.session.query(extract('month', Expense.date)).distinct().filter(extract('year', Expense.date) == year).all()]	
	
	spenderChoices = [u.username for u in db.session.query(User.username).all()]
	spenderChoices.append("All")	
	monthlyForm.spender.choices = spenderChoices
	if spender is None:
		monthlyForm.spender.process_data("All")
	else:
		monthlyForm.spender.process_data(spender)
		
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
		flash(f"Created a new expense record", "info")
		return redirect(url_for('home'))
	return render_template('index.html', newExpenseForm=newExpenseForm)   
    
@app.route("/configure", methods=["GET","POST"])
def configure():
	newUserForm = forms.NewUserForm()
	newCategoryForm = forms.NewCategoryForm()
	if newUserForm.validate_on_submit():		
		if bool(db.session.query(User).filter(User.username == newUserForm.username.data).first()):
			flash(f"Error adding new user.  '{newUserForm.username.data}' already exists.", "danger")
		else:
			user = User(username=newUserForm.username.data)
			db.session.add(user)
			db.session.commit()
			flash(f"User '{user.username}' has been successfully added", "success")
		return redirect(url_for('configure'))
	if newCategoryForm.validate_on_submit():		
		if bool(db.session.query(Category).filter(Category.expenseCategory == newCategoryForm.category.data).first()):
			flash(f"Error adding new category.  '{newCategoryForm.category.data}' already exists.", "danger")
		else:		
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
		flash(f"Error: Unable to delete '{deletedCategory}'.  It is being used in one or more records.", "danger")
	else:				
		Category.query.filter(Category.categoryId == categoryId).delete()
		db.session.commit()
		flash(f"Category '{deletedCategory}' has been successfully removed", "success")
	return redirect(url_for('configure'))
	
@app.route("/deleteUser/<userId>", methods=["GET","POST"])
def deleteUser(userId):
	deletedUser = User.query.filter(User.userId == userId).first().username
	
	if bool(db.session.query(Expense).filter(Expense.spenderId == userId).first()):
		flash(f"Error: Unable to delete '{deletedUser}'.  It is being used in one or more records.", "danger")	
	else:
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
