from flask import Markup, url_for
import datetime

def getExpenseTable(Expense, Category, User):		
	expenses = Expense.query.all()
	print(expenses)
	
	tableHeaders = ['Date', 'Spender', 'Category', 'Amount', 'Description']
	
	table = "<table border=1>"	
	
	table += "<thead><tr>"
	for item in tableHeaders:
		table += "<th>" + item + "</th>"
	table += "</tr></thead>"
	
	for expense in expenses:
		formattedDate = expense.date.strftime("%B %d, %Y")
		print(f"Charlie: Type: {type(expense.date)}")
		table += "<tr>"
		table += "<td>" + str(formattedDate) + "</td>"
		table += "<td>" + expense.spender.username + "</td>"
		table += "<td>" + expense.myCategory.expenseCategory + "</td>"
		table += "<td>$" + str("{:.2f}".format(expense.amount)) + "</td>"
		table += "<td>" + expense.description + "</td>"
		table += "<td>(<a href=deleteExpense/" + str(expense.expenseId) + ">Delete</a>)</td>"
	
	table += "</table>"
		
	return Markup(table)
	
	
	
#<table>
#<tbody>
#<tr><td>Name1</td><td>Description1</td></tr>
#<tr><td>Name2</td><td>Description2</td></tr>
#<tr><td>Name3</td><td>Description3</td></tr>
#</tbody>
#</table>
