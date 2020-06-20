from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField, DecimalField, BooleanField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, NumberRange
from tracker_app.models import Category, User
from datetime import date

class ExpenseConfigureForm(FlaskForm):
	yearChoices = [2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024]
	monthChoices = [(1,'January'), (2,'February'), (3,'March'), (4,'April'), (5,'May'), (6,'June'),
					(7, 'July'), (8,'August'), (9,'September'), (10,'October'), (11,'November'), (12,'December')]
	year = SelectField('Year', choices=yearChoices, validate_choice=False)
	month = SelectField('Month', choices=monthChoices, validate_choice=False)
	submit = SubmitField('Show Expenses')

class NewExpenseForm(FlaskForm):
	# Get list of categories for category pull down		
	date = DateField('Expense Date', validators=[DataRequired()], default=date.today)
	expenseCategory = SelectField('Expense Category', validators=[DataRequired()], validate_choice=False)
	spender = SelectField('Spender', validators=[DataRequired()], validate_choice=False)
	amount = DecimalField('Amount', places=2, validators=[DataRequired(message='Amount must be in monetary format')])
	description = TextAreaField('Description', render_kw={"placeholder": "Transaction details"})
	submit = SubmitField('Create Expense')

class NewCategoryForm(FlaskForm):
	category = StringField('Expense Category', validators=[DataRequired()])
	discretionary = BooleanField('Discretionary', default=False)
	submit = SubmitField('Create Category')

class NewUserForm(FlaskForm):
	username = 	StringField('Spender name', validators=[DataRequired()])
	submit = SubmitField('Create Spender')
