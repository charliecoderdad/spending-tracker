from flask import Markup, url_for
from tracker_app.models import Expense, Metadata
import datetime
from sqlalchemy import and_, func, extract
import calendar, datetime
from tracker_app import db
#from tracker_app.models import Expense


class AnalyzeData():
	def __init__(self, year):
		self.year = int(year)
		self.isCurrentYear = bool(int(year) == datetime.datetime.today().year)
		self.startDate = self.getStartDate()
		self.endDate = self.getEndDate()
		self.num_days = (self.endDate - self.startDate).days
		
	def getAnalysisStats(self):
		total = Expense.query.with_entities(func.sum(Expense.amount)).filter(extract('year', Expense.date)==self.year).scalar()		
		expenses = db.session.query(Expense).filter(extract('year', Expense.date) == self.year).all()				
		discTotal = 0
		for expense in expenses:
			if (expense.myCategory.discretionary):
				discTotal += expense.amount
		requiredTotal = total - discTotal				
							
		daysInyear = 366 if calendar.isleap(self.year) else 365
		stats = "<b>Total Spent: $" + str("{:,.2f}".format(total) + "</b>")
		stats += "<br>Total Discretionary Spending: $" + str("{:,.2f}".format(discTotal))
		stats += "<br>Minimum Required spending: $" + str("{:.2f}".format(requiredTotal))
		if (self.isCurrentYear):
			dailyAvg = total / self.num_days
			reqDailyAvg = requiredTotal / self.num_days
		else:
			dailyAvg = total / daysInyear
			reqDailyAvg = requiredTotal / daysInyear
		stats += "<br>Average daily spending: $" + str("{:,.2f}".format(dailyAvg))
		
		if (self.isCurrentYear):
			stats += "<br><br><b>Projected yearly spending: $" + str("{:,.2f}".format(dailyAvg * daysInyear) + "</b>")
			stats += "<br>Projected minimal spending: $" + str("{:,.2f}".format(reqDailyAvg * daysInyear) + "</b>")
		return Markup(stats)		
	
	def getEndDate(self):
		if (self.isCurrentYear == "False"):
			return datetime.date(self.year, 12, 31)
		else:
			return datetime.date(self.year, datetime.datetime.today().month, datetime.datetime.today().day)
	
	def getStartDate(self):
		month = Metadata.query.with_entities(func.min(Metadata.monthNum)).filter(Metadata.year == self.year).scalar()
		if (month == 1 or self.isCurrentYear == "False"):
			return datetime.date(self.year, 1, 1)
		else:
			my_num_days = calendar.monthrange(self.year, int(month))[1]
			start_date = datetime.date(self.year, int(month), 1)
			end_date = datetime.date(self.year, int(month), my_num_days)		
			day = Expense.query.filter(and_(
							Expense.date >= start_date,
							Expense.date <= end_date
						)).first().date.day
			return datetime.date(self.year, int(month), int(day))
			
		
	def getAnalyzeTable(self):
		expenses = self.expenses
		
		# Generate categories dict
		catDict = {}
		total = 0
		for e in expenses:
			total += e.amount
			if e.myCategory.expenseCategory not in catDict:
				catDict[e.myCategory.expenseCategory] = {}
				catDict[e.myCategory.expenseCategory]["total"] = e.amount
				catDict[e.myCategory.expenseCategory]["percent"] = 0
			else:
				catDict[e.myCategory.expenseCategory]["total"] += e.amount
		#calc percent in categories dict
		for cat in catDict:
			catDict[cat]["percent"] = catDict[cat]["total"] / total * 100
			
		
		tableHeaders = ['Category', 'Total', 'Percent']
		table = "Analysis"
		table += "<table border=1>"
		table += "<thead><tr>"
		for item in tableHeaders:
			table += "<th>" + item + "</th>"
		table += "</tr></thead>"	
		for cat in catDict:
			table += "<tr>"
			table += "<td>" + cat + "</td>"
			table += "<td>$" + str("{:.2f}".format(catDict[cat]['total'])) + "</td>"
			table += "<td>" + str("{:.2f}".format(catDict[cat]['percent'])) + "%</td>"
		table += "</table>"
		
		return Markup(table)

	def getExpenseTable(self):	
		expenses = self.expenses
		tableHeaders = ['Date', 'Spender', 'Category', 'Amount', 'Description']			
		table = "Expenses - " + str(expenses.count()) + " records"
		table += "<table border=1>"
		table += "<thead><tr>"
		for item in tableHeaders:
			table += "<th>" + item + "</th>"
		table += "</tr></thead>"	
		for expense in expenses:
			formattedDate = expense.date.strftime("%B %d, %Y")
			table += "<tr>"
			table += "<td>" + str(formattedDate) + "</td>"
			table += "<td>" + expense.spender.username + "</td>"
			table += "<td>" + expense.myCategory.expenseCategory + "</td>"
			table += "<td>$" + str("{:.2f}".format(expense.amount)) + "</td>"
			table += "<td>" + expense.description + "</td>"
			table += "<td>(<a href= " + url_for('deleteExpense', expenseId=expense.expenseId) + ">Delete</a>)</td>"	
		table += "</table>"
		
		return Markup(table)
