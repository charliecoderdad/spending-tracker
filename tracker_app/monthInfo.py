from flask import Markup, url_for
from tracker_app.models import Expense, User
from sqlalchemy import and_
import calendar, datetime
from collections import OrderedDict
from tracker_app import helpers, db

class MonthInfo():
	def __init__(self, year, month, spender=None):
		self.year = year
		self.month = month

		self.num_days = calendar.monthrange(int(self.year), int(self.month))[1]
		start_date = datetime.datetime(int(self.year), int(self.month), 1)
		end_date = datetime.datetime(int(self.year), int(self.month), self.num_days)
		self.isCurrentMonth = bool(int(year) == datetime.datetime.today().year and int(month) == datetime.datetime.today().month)
		self.spender = spender
		if self.spender == "All":
			self.spender = None
		if self.spender is None:
			self.expenses = db.session.query(Expense).filter(and_(
						Expense.date >= start_date,
						Expense.date <= end_date
					)).order_by(Expense.date.desc()).all()		
		else:
			self.expenses = db.session.query(Expense).join(User).filter(and_(
						Expense.date >= start_date,
						Expense.date <= end_date,
						User.username == self.spender
					)).order_by(Expense.date.desc()).all()
		
	def getMonthlyExpenseStats(self):
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

	def getExpenseTable(self):	
		expenses = self.expenses
		tableHeaders = ['Date', 'Spender', 'Category', 'Amount', 'Description', '']
		table = "Expenses - " + str(len(expenses)) + " records"
		table += helpers.getTableHeadTags(tableHeaders)		
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
