from flask import Markup, url_for
from tracker_app.models import Expense, User
from tracker_app import helpers
import datetime
from sqlalchemy import and_, extract
import calendar, datetime
from tracker_app import db
from collections import OrderedDict


class CategoryTable():
	def __init__(self, year, month=None, spender=None):
		self.year = int(year)
		if month is not None:
			self.month = int(month)
		else:
			self.month = None
		self.spender = spender
		if self.spender == "All":
			self.spender = None
		
		
	def getCategoryAnalysisTable(self):
		
		# If no month arg passed into class then we need expenses for entire year, else get for single month
		if (self.month is None):
			if (self.spender is None):
				expenses = db.session.query(Expense).filter(extract('year', Expense.date) == self.year).all()
			else:
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
		table = ""
		if (self.month == -1):
			table += f" for {self.year}" 

		table += helpers.getTableHeadTags(tableHeaders)		
		for cat in catDict:
			table += "<tr>"
						
			# Need to get the link for the search based on entire year
			if self.spender is None:
				mySpender = "nodata"
			else:
				mySpender = self.spender
			if self.month is None:
				myStart = datetime.date(self.year, 1, 1)
				myEnd = datetime.date(self.year, 12, 31)
				link = url_for('search', startDate=myStart, endDate=myEnd, category=cat, spender=mySpender, descText="nodata")
			else:
				#Need to get link for the search based on current month
				myStart = datetime.date(self.year, self.month, 1)
				myNumDays = calendar.monthrange(self.year, self.month)[1]
				myEnd = datetime.date(self.year, self.month, myNumDays)				
				link = url_for('search', startDate=myStart, endDate=myEnd, category=cat, spender=mySpender, descText="nodata")
			table += "<td><a href=" + link + " class='catlink'>" + str(cat) + "</a></td>"
			table += "<td>$" + str("{:,.2f}".format(catDict[cat]['total'])) + "</td>"
			table += "<td>" + str("{:,.2f}".format(catDict[cat]['percent'])) + "%</td>"
		table += "</table>"
		
		return Markup(table)
