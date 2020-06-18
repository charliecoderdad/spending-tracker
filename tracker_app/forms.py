from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField, DecimalField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, NumberRange
from tracker_app.models import Category, User
from datetime import date

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
	submit = SubmitField('Add New Expense Category')

class NewUserForm(FlaskForm):
	username = 	StringField('User name', validators=[DataRequired()])
	submit = SubmitField('Add New User')
