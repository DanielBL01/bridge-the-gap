from flask import Flask, render_template, redirect, url_for

from wtform import *
from models import *

# Configure app
app = Flask(__name__)
app.secret_key = 'SECRET KEY'

# Configure database hosted by Heroku
app.config['SQLALCHEMY_DATABASE_URI'] = 'SECRET HEROKU DATABASE URI'
db = SQLAlchemy(app)

@app.route("/", methods=['GET', 'POST'])
def index():
	'''route url_for('index')'''

	registration_form = RegistrationForm()

	# User is processed into database on valid form submit -> redirect to login page
	if registration_form.validate_on_submit():
		username = registration_form.username.data
		password = registration_form.password.data

		# Save user to database
		user = User(username=username, password=password)
		db.session.add(user)
		db.session.commit()

		return redirect(url_for('login'))
		
	return render_template("index.html", my_form = registration_form)

@app.route("/login", methods=['GET', 'POST'])
def login():
	'''route url_for('login')'''

	login_form = LoginForm()

	if login_form.validate_on_submit():
		return "Welcome to Bridge the Gap!"

	# Handling case if user uses GET method to visit login page
	return render_template("login.html", my_form=login_form)
if __name__ == "__main__":
	app.run(debug=True)
