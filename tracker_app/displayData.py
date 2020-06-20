from flask import Markup, url_for
import datetime

class DisplayData():
	def __init__(self, expenses):
		self.expenses = expenses
		
	def getPage(self):
		html = self.getExpenseStats(self.expenses)
		html += self.getExpenseTable(self.expenses)
		return Markup(html)

	def getExpenseStats(self, expenses):
		stats = "Placeholder"
		return stats

	def getExpenseTable(self, expenses):
		
		tableHeaders = ['Date', 'Spender', 'Category', 'Amount', 'Description']	
		table = "<table border=1>"
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
			table += "<td>(<a href=deleteExpense/" + str(expense.expenseId) + ">Delete</a>)</td>"	
		table += "</table>"
		
		return table
