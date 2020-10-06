from flask import Flask, render_template

from wtform import *

app = Flask(__name__)
app.secret_key = 'replace later'

@app.route("/", methods=['GET', 'POST'])
def index():
	
	registration_form = RegistrationForm()
	if registration_form.validate_on_submit():
		return "Welcome to Bridge the Gap"
		
	return render_template("index.html", my_form = registration_form)

if __name__ == "__main__":
	app.run(debug=True)
