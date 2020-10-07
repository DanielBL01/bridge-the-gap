from flask import Flask, render_template

from wtform import *
from models import *

# Configure app
app = Flask(__name__)
app.secret_key = 'replace later'

# Configure database hosted by Heroku
app.config['SQLALCHEMY_DATABASE_URI'] = 'My Heroku PostgreSQL URI'
db = SQLAlchemy(app)

@app.route("/", methods=['GET', 'POST'])
def index():
	
	registration_form = RegistrationForm()

	if registration_form.validate_on_submit():
		username = registration_form.username.data
		password = registration_form.password.data

		# Find user in database
		user_obj = User.query.filter_by(username=username).first()
		
		if user_obj:
			return "This username is already taken! Try again :)"

		# Save user to database
		user = User(username=username, password=password)
		db.session.add(user)
		db.session.commit()
		return "Saved to our database. Time to log in!"
		
	return render_template("index.html", my_form = registration_form)

if __name__ == "__main__":
	app.run(debug=True)
