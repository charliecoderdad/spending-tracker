from flask import Markup, url_for
import datetime

class DisplayData():
	def __init__(self, expenses):
		self.expenses = expenses
		
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
		#isCurrentMonth = expenses.query.first().date.year		
		return Markup(stats)

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
