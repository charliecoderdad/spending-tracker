from flask import Markup

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
		print(f"Leggo {expense.amount}")
		table += "<tr>"
		table += "<td>" + str(expense.date) + "</td>"
		table += "<td>" + expense.spender.username + "</td>"
		table += "<td>" + expense.myCategory.expenseCategory + "</td>"
		table += "<td>" + str(expense.amount) + "</td>"
		table += "<td>" + expense.description + "</td>"
		table += "</tr>"
	
	table += "</table>"
		
	return Markup(table)
	
	
	
#<table>
#<tbody>
#<tr><td>Name1</td><td>Description1</td></tr>
#<tr><td>Name2</td><td>Description2</td></tr>
#<tr><td>Name3</td><td>Description3</td></tr>
#</tbody>
#</table>
