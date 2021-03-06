from flask import Markup, url_for
from tracker_app.models import Expense, Category, User
from tracker_app import helpers
from sqlalchemy import and_, func, extract
import calendar, datetime
from tracker_app import db


class YearInfo():
	def __init__(self, year, spender=None):
		self.year = int(year)
		self.isCurrentYear = bool(int(year) == datetime.datetime.today().year)
		self.startDate = self.getStartDate()
		self.endDate = self.getEndDate()
		self.num_days = (self.endDate - self.startDate).days + 1
		self.curr_days = (datetime.datetime.today() - datetime.datetime.combine(self.startDate, datetime.datetime.min.time())).days + 1
		self.spender = spender
		if (self.spender == "All"):
			self.spender = None

	def breakdownByMonthAnalysisTable(self):
		#months = db.session.query(extract('month', Expense.date)).filter(extract('year', Expense.date)==self.year).distinct().all()
		months = db.session.query(extract('month', Expense.date)).filter(extract('year', Expense.date)==self.year).order_by(Expense.date).distinct(extract('year', Expense.date)).all()
		months = [i[0] for i in months]
		
		tableHeaders = ['Month', 'Total', 'Min. Spending', 'Discretionary']
		table = ""
		table += helpers.getTableHeadTags(tableHeaders)		
		for month in months:
			# If no spender specified we can sum all records for the given year/month
			if (self.spender is None):
				monthTotal = db.session.query(
					func.sum(Expense.amount)).filter(
						and_(
							extract('year', Expense.date) == self.year,
							extract('month', Expense.date) == month)
						).scalar()
						
				monthMinSpendTotal = db.session.query(
					func.sum(Expense.amount)).join(Category).filter(
						and_(
							Category.discretionary == False,
							extract('year', Expense.date) == self.year,
							extract('month', Expense.date) == month)
						).scalar()
			# else if a spender id is provided we need to sum based on spender 
			else:
				monthTotal = db.session.query(
					func.sum(Expense.amount)).join(User).filter(
						and_(
							extract('year', Expense.date) == self.year,
							extract('month', Expense.date) == month),
							User.username == self.spender
						).scalar()
						
				monthMinSpendTotal = db.session.query(
					func.sum(Expense.amount)).join(Category).join(User).filter(
						and_(
							Category.discretionary == False,
							extract('year', Expense.date) == self.year,
							extract('month', Expense.date) == month),
							User.username == self.spender
						).scalar()
				
			if monthMinSpendTotal is None:
				monthMinSpendTotal = 0
			if monthTotal is None:
				monthTotal = 0
			monthDiscSpendTotal = monthTotal - monthMinSpendTotal
			
			table += "<tr>"
			table += "<td>" + str(calendar.month_name[month]) + "</td>"
			table += "<td>$" + str("{:,.2f}".format(monthTotal)) + "</td>"
			table += "<td>$" + str("{:,.2f}".format(monthMinSpendTotal)) + "</td>"
			table += "<td>$" + str("{:,.2f}".format(monthDiscSpendTotal)) + "</td>"
			table += "</tr>"
		table += "</table>"		
		return Markup(table)
		
	def getYearlyStats(self):
		queries = []
		queries.append(extract('year', Expense.date)==self.year)
		if self.spender is not None:
			queries.append(User.username == self.spender)
				
		total = db.session.query(func.sum(Expense.amount)).join(User).filter(and_(*queries)).scalar()
		expenses = db.session.query(Expense).join(User).filter(and_(*queries)).all()
					
		discTotal = 0
		for expense in expenses:
			if (expense.myCategory.discretionary):
				discTotal += expense.amount
		if total is None:
			total = 0
		if discTotal is None:
			discTotal = 0
		requiredTotal = total - discTotal				
							
		daysInyear = 366 if calendar.isleap(self.year) else 365
		if (self.isCurrentYear):
			dailyAvg = total / self.num_days
			reqDailyAvg = requiredTotal / self.num_days
		else:
			dailyAvg = total / daysInyear
			reqDailyAvg = requiredTotal / daysInyear	
		
		stats = "<table class='table table-sm'>"
		stats += "<tr><td><b>Total</b></td><td><b>$" + str("{:,.2f}".format(total)) + "</b></td.</tr>"
		stats += "<tr><td>Minimum Amount Spent</td><td>$" + str("{:,.2f}".format(requiredTotal)) + "</td.</tr>"
		stats += "<tr><td>Discretionary Amount Spent</td><td>$" + str("{:,.2f}".format(discTotal)) + "</td.</tr>"
		stats += "<tr><td>Avg. Daily Spending (through " + str(self.curr_days) + " days)</td><td>$" + str("{:,.2f}".format(dailyAvg)) + "</td.</tr>"
		if self.isCurrentYear:
			stats += "<tr><td>Projected Final Yearly Spending</td><td>$" + str("{:,.2f}".format(dailyAvg * daysInyear)) + "</td.</tr>"
			stats += "<tr><td>Projected Final Minimal Yearly Spending</td><td>$" + str("{:,.2f}".format(reqDailyAvg * daysInyear)) + "</td.</tr>"
		stats += "</table>"
	
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
		month = db.session.query(func.min(extract('month', Expense.date))).filter(extract('year', Expense.date)==self.year).distinct().scalar()
		if bool(month) == False:
			return datetime.date.today()
		if (month == 1 or self.isCurrentYear == "False"):
			return datetime.date(self.year, 1, 1)
		else:
			firstExpRecord = db.session.query(func.min(Expense.date)).filter(extract('year', Expense.date) == self.year).first()[0]
			return firstExpRecord.date()
