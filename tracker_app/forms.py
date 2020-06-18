from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class NewUserForm(FlaskForm):
	username = 	StringField('User name', validators=[DataRequired()])
	submit = SubmitField('Add New User')
