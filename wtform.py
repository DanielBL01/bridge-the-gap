from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, EqualTo

class RegistrationForm(FlaskForm):
	'''
	Registration Form

	Using WTForms to validate registration.
	username: required and must be 4-20 characters long
	password: required and must be 4-20 characters long
	password_confirm = must match password
	'''

	username = StringField('username_label',
		validators=[InputRequired(message="Username required"),
		Length(min=4, max=20, message="Username must be between 4-20 characters")])

	password = PasswordField('password_label',
		validators=[InputRequired(message="Password required"),
		Length(min=4, max=20, message="Password must be between 4-20 characters")])

	password_confirm = PasswordField('password_confirm_label',
		validators=[InputRequired(message="Confirmation required"),
		EqualTo('password', message="Passwords must match")])

	submit_button = SubmitField('Create')
