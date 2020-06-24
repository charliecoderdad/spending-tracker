from flask import Markup, url_for
from tracker_app.models import Expense, Metadata, User
from tracker_app import helpers
import datetime
from sqlalchemy import and_, func, extract
import calendar, datetime
from tracker_app import db
from collections import OrderedDict


class CategoryTable():
	def __init__(self, year, month=None, spender=None):
		self.year = int(year)	
		self.month = month
		self.spender = spender
		if self.spender == "All":
			self.spender = None
		
		
	def getCategoryAnalysisTable(self):
		
		# If no month arg passed into class then we need expenses for entire year, else get for single month
		if (self.month is None):
			if (self.spender is None):
				expenses = db.session.query(Expense).filter(extract('year', Expense.date) == self.year).all()
			else:
				print(f"\n\nSelf spender: {self.spender}")
				expenses = db.session.query(Expense).join(User).filter(and_(
						extract('year', Expense.date) == self.year,
						User.username == self.spender
						)).all()
		# Else we are looking for expenses for specific month
		else:
			if (self.spender is None):
				expenses = db.session.query(Expense).filter(and_(
						extract('year', Expense.date) == self.year),
						extract('month', Expense.date) == self.month).all()
			else:
				expenses = db.session.query(Expense).join(User).filter(and_(
						extract('year', Expense.date) == self.year,
						extract('month', Expense.date) == self.month,
						User.username == self.spender
						)).all()
		
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
			
		# TODO: Sort the catDic by total		
		catDict = OrderedDict(sorted(catDict.items(), key = lambda x: (int(x[1]['percent'])), reverse=True))
		
		tableHeaders = ['Category', 'Total', 'Percent']
		table = f"Categorical Analysis"
		if (self.month == -1):
			table += f" for {self.year}" 

		table += helpers.getTableHeadTags(tableHeaders)		
		for cat in catDict:
			table += "<tr>"
			table += "<td>" + str(cat) + "</td>"
			table += "<td>$" + str("{:,.2f}".format(catDict[cat]['total'])) + "</td>"
			table += "<td>" + str("{:,.2f}".format(catDict[cat]['percent'])) + "%</td>"
		table += "</table>"
		
		return Markup(table)
		
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
