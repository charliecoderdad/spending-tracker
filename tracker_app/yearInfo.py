from flask import Markup, url_for
from tracker_app.models import Expense, Metadata
from sqlalchemy import and_, func, extract
import calendar, datetime
from tracker_app import db


class YearInfo():
	def __init__(self, year):
		self.year = int(year)
		self.isCurrentYear = bool(int(year) == datetime.datetime.today().year)
		self.startDate = self.getStartDate()
		self.endDate = self.getEndDate()
		self.num_days = (self.endDate - self.startDate).days		
		
	def getYearlyStats(self):
		total = Expense.query.with_entities(func.sum(Expense.amount)).filter(extract('year', Expense.date)==self.year).scalar()		
		expenses = db.session.query(Expense).filter(extract('year', Expense.date) == self.year).all()				
		discTotal = 0
		for expense in expenses:
			if (expense.myCategory.discretionary):
				discTotal += expense.amount
		requiredTotal = total - discTotal				
							
		daysInyear = 366 if calendar.isleap(self.year) else 365
		stats = "<b>Total Spent: $" + str("{:,.2f}".format(total) + "</b>")
		stats += "<br>Total Discretionary Spending: $" + str("{:,.2f}".format(discTotal))
		stats += "<br>Minimum Required spending: $" + str("{:.2f}".format(requiredTotal))
		if (self.isCurrentYear):
			dailyAvg = total / self.num_days
			reqDailyAvg = requiredTotal / self.num_days
		else:
			dailyAvg = total / daysInyear
			reqDailyAvg = requiredTotal / daysInyear
		stats += "<br>Average daily spending: $" + str("{:,.2f}".format(dailyAvg))
		
		if (self.isCurrentYear):
			stats += "<br><br><b>Projected yearly spending: $" + str("{:,.2f}".format(dailyAvg * daysInyear) + "</b>")
			stats += "<br>Projected minimal spending: $" + str("{:,.2f}".format(reqDailyAvg * daysInyear) + "</b>")
		return Markup(stats)		
	
	###
	### Returns 12/31 of the year if year under analysis is not current year, else returns current days date
	###
	def getEndDate(self):
		if (self.isCurrentYear == "False"):
			return datetime.date(self.year, 12, 31)
		else:
			return datetime.date(self.year, datetime.datetime.today().month, datetime.datetime.today().day)
	
	###
	### Use this if starting budget in middle of the year.. otherwise return Jan 1st of the year under analysis
	###
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
