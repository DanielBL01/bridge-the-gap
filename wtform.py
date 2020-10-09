from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, EqualTo, ValidationError

from passlib.hash import pbkdf2_sha256
from models import User

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

	def validate_username(self, username):
		'''
		Custom validation to check for duplicate usernames

		Parameters:
		username: username field POST data
		'''
		user_object = User.query.filter_by(username=username.data).first()
		if user_object:
			raise ValidationError("This Username is already taken! Try a different username")

class LoginForm(FlaskForm):
	'''Login Form'''

	username = StringField('username_label', 
		validators=[InputRequired(message="Username is required")])

	password = StringField('password_label',
		validators=[InputRequired(message="Password is required")])

	submit_button = SubmitField('Login')

	def validate_password(form, field):
		user_password_entered = field.data
		user_username_entered = form.username.data

		user_object = User.query.filter_by(username=user_username_entered).first()
		if user_object is None:
			raise ValidationError("Username or password is incorrect")
		
		elif not pbkdf2_sha256.verify(user_password_entered, user_object.password):
			raise ValidationError("Username or password is incorrect")


		
