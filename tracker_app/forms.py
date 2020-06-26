from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField, DecimalField, BooleanField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Optional, ValidationError
from tracker_app.models import Expense
from tracker_app import db
from sqlalchemy import extract
import datetime

class SearchForm(FlaskForm):
	startDate = DateField('Start Date', default="", validators=[Optional()])
	endDate = DateField('End Date', default="", validators=[Optional()])
	expenseCategory = SelectField('Category', validate_choice=False)
	spender = SelectField('Spender', validate_choice=False)
	descText = StringField('Description')
	submit = SubmitField('Search')

class EditExpenseForm(FlaskForm):
	# Get list of categories for category pull down		
	date = DateField('Expense Date', validators=[DataRequired()], default=datetime.date.today)
	expenseCategory = SelectField('Expense Category', validators=[DataRequired()], validate_choice=False)
	spender = SelectField('Spender', validators=[DataRequired()], validate_choice=False)
	amount = DecimalField('Amount', places=2, validators=[DataRequired(message='Amount must be in monetary format')])
	description = TextAreaField('Description', render_kw={"placeholder": "Transaction details"})
	submit = SubmitField('Edit Expense')

class YearlyAnalysisConfigureForm(FlaskForm):
	year = SelectField('Year', validate_choice=False)
	spender = SelectField('Spender', choices=["All"], validate_choice=False, default="All")
	submit = SubmitField('Update')

class MonthlyAnalysisConfigureForm(FlaskForm):
	month_choices = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
	year = SelectField('Year', validate_choice=False, default=datetime.datetime.today().year)
	month = SelectField('Month', choices=month_choices, validate_choice=False, default=datetime.datetime.today().month)
	spender = SelectField('Spender', choices=["All"], validate_choice=False, default="All")
	submit = SubmitField('Update')

class NewExpenseForm(FlaskForm):
	# Get list of categories for category pull down		
	date = DateField('Expense Date', validators=[DataRequired()], default=datetime.date.today)
	expenseCategory = SelectField('Expense Category', validators=[DataRequired()], validate_choice=False)
	spender = SelectField('Spender', validators=[DataRequired()], validate_choice=False)
	amount = DecimalField('Amount', places=2, validators=[DataRequired(message='Amount must be a number')])
	description = TextAreaField('Description', render_kw={"placeholder": "Transaction details"})
	submit = SubmitField('Create Expense')

def verifyNoSlashes(form, field):
	if "/" in field.data:
		raise ValidationError("Field must not contain '/' character")

class NewCategoryForm(FlaskForm):
	category = StringField('Category', validators=[DataRequired(), verifyNoSlashes])
	discretionary = BooleanField('Discretionary', default=False)
	submitCat = SubmitField('Create Category')
	
		

class NewUserForm(FlaskForm):
	username = 	StringField('Spender', validators=[DataRequired(), verifyNoSlashes])
	submitUser = SubmitField('Create Spender')
