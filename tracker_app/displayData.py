from flask import Markup, url_for
from tracker_app.models import Expense
import datetime
from sqlalchemy import and_
import calendar, datetime

class DisplayData():
	def __init__(self, year, month):
		self.year = year
		self.month = month

		self.num_days = calendar.monthrange(int(self.year), int(self.month))[1]
		start_date = datetime.date(int(self.year), int(self.month), 1)
		end_date = datetime.date(int(self.year), int(self.month), self.num_days)		
		self.expenses = Expense.query.filter(and_(
						Expense.date >= start_date,
						Expense.date <= end_date
					)).order_by(Expense.date.desc())
		self.isCurrentMonth = bool(int(year) == datetime.datetime.today().year and int(month) == datetime.datetime.today().month)
		
	def getExpenseStats(self):
		expenses = self.expenses
		total = 0
		discretionarySpending = 0
		requiredSpending = 0
		for expense in expenses:
			total += expense.amount
			if (expense.myCategory.discretionary):
				discretionarySpending += expense.amount
			else:
				requiredSpending += expense.amount
			
		stats = "<b>Total: $" + str("{:.2f}".format(total) + "</b>")
		stats += "<br>Discretionary spending: $" + str("{:.2f}".format(discretionarySpending))
		stats += "<br>Required spending: $" + str("{:.2f}".format(requiredSpending))
		if (self.isCurrentMonth):
			dailyAvg = total / datetime.datetime.today().day
		else:
			dailyAvg = total / self.num_days
		stats += "<br>Average daily spending: $" + str("{:.2f}".format(dailyAvg))
		
		if (self.isCurrentMonth):
			stats += "<br><br>Projected final spending: $" + str("{:.2f}".format(dailyAvg * self.num_days))
		return Markup(stats)		
		
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
