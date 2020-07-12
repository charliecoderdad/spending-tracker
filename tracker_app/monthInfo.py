from flask import Markup, url_for
from tracker_app.models import Expense, User
from sqlalchemy import and_
import calendar, datetime
from collections import OrderedDict
from tracker_app import helpers, db

class MonthInfo():
	def __init__(self, year, month, spender=None):
		self.year = int(year)
		self.month = month

		self.num_days = calendar.monthrange(int(self.year), int(self.month))[1]
		self.curr_days = datetime.datetime.today().day
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
					)).order_by(Expense.date.desc(), Expense.expenseId.desc()).all()		
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
				
		if (self.isCurrentMonth):
			dailyAvg = total / datetime.datetime.today().day
		else:
			dailyAvg = total / self.num_days

		stats = "<table class='table table-sm'>"
		stats += "<tr><td><b>Total</b></td><td><b>$" + str("{:,.2f}".format(total)) + "</b></td.</tr>"
		stats += "<tr><td>Minimum Amount Spent</td><td>$" + str("{:,.2f}".format(requiredSpending)) + "</td.</tr>"
		stats += "<tr><td>Discretionary Amount Spent</td><td>$" + str("{:,.2f}".format(discretionarySpending)) + "</td.</tr>"
		stats += "<tr><td>Avg. Daily Spending (through " + str(self.curr_days) + " days)</td><td>$" + str("{:,.2f}".format(dailyAvg)) + "</td.</tr>"
		if (self.isCurrentMonth):
			stats += "<tr><td>Projected Final Spending</td><td>$" + str("{:,.2f}".format(dailyAvg * self.num_days)) + "</td.</tr>"
		daysInyear = 366 if calendar.isleap(self.year) else 365
		stats += "<tr><td>Projected Yearly Spending</td><td>$" + str("{:,.2f}".format(dailyAvg * daysInyear)) + "</td.</tr>"
		stats += "</table>"
		return Markup(stats)		

	def getExpenseTable(self):	
		expenses = self.expenses
		tableHeaders = ['Date', 'Spender', 'Category', 'Amount', 'Description', '']
		
		table = helpers.getTableHeadTags(tableHeaders)		
		for expense in expenses:
			formattedDate = expense.date.strftime("%B %d, %Y")
			table += "<tr>"
			table += "<td style='white-space:nowrap'>" + str(formattedDate) + "</td>"
			table += "<td style='white-space:nowrap'>" + expense.spender.username + "</td>"
			table += "<td style='white-space:nowrap'>" + expense.myCategory.expenseCategory + "</td>"
			table += "<td style='white-space:nowrap'>$" + str("{:,.2f}".format(expense.amount)) + "</td>"
			table += "<td>" + expense.description + "</td>"
			table += "<td style='text-align:center' style='white-space:nowrap' width=80>"
			table += "<a href= " + url_for('editExpense', expenseId=expense.expenseId) + "><img src=" + url_for('static', filename='edit.png') + " width='25' height='25' title='Edit Record'></a>"
			table += "<a href='#deleteConfirmModal' data-toggle='modal' onClick='expenseIdToDelete(" + str(expense.expenseId) + ")'><img src=" + url_for('static', filename='delete.png') + " width='25' height='25' title='Delete Record'></a>"
			table += "</td>"	
		table += "</table>"
		table += "Expenses - " + str(len(expenses)) + " records"
		
		return Markup(table)
