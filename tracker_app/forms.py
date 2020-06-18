from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class NewCategoryForm(FlaskForm):
	category = StringField('Expense Category', validators=[DataRequired()])
	submit = SubmitField('Add New Expense Category')

class NewUserForm(FlaskForm):
	username = 	StringField('User name', validators=[DataRequired()])
	submit = SubmitField('Add New User')
