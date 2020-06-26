from flask import Markup, url_for
from tracker_app.models import Expense, User, Category
from sqlalchemy import and_, func
import calendar, datetime
from collections import OrderedDict
from tracker_app import helpers, db

class SearchData():
	def __init__(self, startDate="nodata", endDate="nodata", expenseCategory="nodata", spender="nodata", descText="nodata"):
		self.startDate = startDate
		#self.endDate = endDate
		self.endDate = endDate
		if self.endDate != "nodata":
			self.endDate = datetime.datetime.strptime(endDate, "%Y-%m-%d")
			self.endDate = self.endDate.replace(hour=23, minute=59, second=59)
		self.expenseCategory = expenseCategory
		self.spender = spender
		self.descText = descText
		
		queries = []
		
		if self.startDate != "nodata":
			print("appending start date query...")
			queries.append(Expense.date >= self.startDate)			
		if self.endDate != "nodata":
			print("appending end date query...")
			queries.append(Expense.date <= self.endDate)
		if self.expenseCategory != "nodata":
			print("appending category query...")
			catId = db.session.query(Category.categoryId).filter(Category.expenseCategory == self.expenseCategory).first()[0]
			print("Found we should be looking for expenses with cat ID of {catId}\n")
			queries.append(Expense.categoryId == catId)
		if self.spender != "nodata":
			print("appending spender query...")
			spId = db.session.query(User.userId).filter(User.username == self.spender).first()[0]
			queries.append(Expense.spenderId == spId)
		if self.descText != "nodata":
			print("appending description text finder query...")
			queries.append(Expense.description.contains("%" + self.descText + "%"))
		
		self.expenses = db.session.query(Expense).join(Category).join(User).filter(and_(*queries)).order_by(Expense.date.desc()).all()
		self.total = db.session.query(func.sum(Expense.amount)).join(Category).join(User).filter(and_(*queries)).scalar()
		if self.total is None:
			self.total = 0
			
	def getExpenseTable(self):	
		expenses = self.expenses
		tableHeaders = ['Date', 'Spender', 'Category', 'Amount', 'Description', '']
		table = "<br><h3>Total:  $" + str("{:,.2f}".format(self.total)) + "</h3>"
		table += "Expenses - " + str(len(expenses)) + " records"
		table += helpers.getTableHeadTags(tableHeaders)		
		for expense in expenses:
			formattedDate = expense.date.strftime("%B %d, %Y")
			table += "<tr>"
			table += "<td style='white-space:nowrap'>" + str(formattedDate) + "</td>"
			table += "<td style='white-space:nowrap'>" + expense.spender.username + "</td>"
			table += "<td style='white-space:nowrap'>" + expense.myCategory.expenseCategory + "</td>"
			table += "<td style='white-space:nowrap'>$" + str("{:.2f}".format(expense.amount)) + "</td>"
			table += "<td>" + expense.description + "</td>"
			table += "<td style='text-align:center' width='80'>"
			table += "<a href= " + url_for('editExpense', expenseId=expense.expenseId) + "><img src=" + url_for('static', filename='edit.png') + " width='25' height='25' title='Edit Record'></a>"
			table += "<a href= " + url_for('deleteExpense', expenseId=expense.expenseId) + "><img src=" + url_for('static', filename='delete.png') + " width='25' height='25' title='Delete Record'></a>"
			table += "</td>"	
		table += "</table>"
		
		return Markup(table)
