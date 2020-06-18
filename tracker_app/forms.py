from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired
from tracker_app.models import Category, User

class NewExpenseForm(FlaskForm):
	# Get list of categories for category pull down	
	
	date = DateField('Expense Date', validators=[DataRequired()])
	category = SelectField('Expense Category', validators=[DataRequired()])
	description = TextAreaField('Description')
	submit = SubmitField('Add New Expense Category')

class NewCategoryForm(FlaskForm):
	category = StringField('Expense Category', validators=[DataRequired()])
	submit = SubmitField('Add New Expense Category')

class NewUserForm(FlaskForm):
	username = 	StringField('User name', validators=[DataRequired()])
	submit = SubmitField('Add New User')
