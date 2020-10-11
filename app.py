from flask import Flask, request, flash, render_template, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from flask_socketio import SocketIO, send, emit, join_room, leave_room
from time import localtime, strftime
from wtform import *
from models import *

# Configure app
app = Flask(__name__)
app.secret_key = 'SECRET KEY'

# Configure database hosted by Heroku
app.config['SQLALCHEMY_DATABASE_URI'] = 'SECRET HEROKU DATABASE URI'
socketio = SocketIO(app)

rooms_list = ["general lounge"]

db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

'''
	Defining the app routes.
	
	The function name under the decorator 
	@app.route define the url_for route.
'''

@app.route("/", methods=['GET', 'POST'])
def index():
	registration_form = RegistrationForm()

	# User is processed into database on valid form submit -> redirect to login page
	if registration_form.validate_on_submit():
		username = registration_form.username.data
		password = registration_form.password.data
		
		# pbkdf2_sha256 module applies both salt and iteration to plain text
		hashed_password = pbkdf2_sha256.hash(password)

		# Save user to database
		user = User(username=username, password=hashed_password)
		db.session.add(user)
		db.session.commit()

		flash('Registered successfully. Please log in.', 'success')
		return redirect(url_for('login'))
	
	# Handling case if user uses GET method to visit homepage
	return render_template("index.html", my_form = registration_form)

@app.route("/login", methods=['GET', 'POST'])
def login():
	'''route url_for('login')'''

	login_form = LoginForm()

	if login_form.validate_on_submit():
		user_object = User.query.filter_by(username=login_form.username.data).first()
		login_user(user_object)
		
		return redirect(url_for('chat'))

	# Handling case if user uses GET method to visit login page
	return render_template("login.html", my_form=login_form)

@app.route("/chat", methods=['GET', 'POST'])
def chat():
	if not current_user.is_authenticated:
		flash('Please login.', 'danger') 
		return redirect(url_for('login'))

	return render_template('chat.html', username=current_user.username, rooms=rooms_list)

@app.route("/logout", methods=['GET'])
def logout():
	
	logout_user()
	flash('You have sucessfully logged out', 'sucess')
	return redirect(url_for('login'))

@app.route("/create_room", methods=['GET', 'POST'])
def create():
	error = None
	if request.method == 'POST':
		room = request.form['room']

		if room in rooms_list:
			error = 'We have bad news... This room name has been taken'

		else:
			rooms_list.append(room)
			return redirect(url_for('chat'))

	return render_template('create_room.html', error=error)

@app.errorhandler(404)
def page_not_found(e):
	'''404 Page not found handler'''

	return render_template('404.html'), 404

'''
	Defining the SocketIO event handlers.

	event handlers send reply messages to connected clients 
	using the send() and emit() functions. We define three 
	events: message, join and leave.

	note: the 'message' event is predefined by SocketIO to define 
	a handler that takes a string payload. Since it's predefined, 
	you need to use the send() function on the client side 
	and emit() for custom events like our 'join' and 'leave'.
'''

@socketio.on('message')
def handle_message(payload):
	print(f'\n{payload}\n')

	msg = payload['msg']
	username = payload['username']
	room = payload['room']

	send({'msg': msg, 'username': username,
		'time': strftime("%b %d, %I:%M%p", localtime())}, room = room)

@socketio.on('join')
def handle_join(data):
	username = data['username']
	room = data['room']

	join_room(room)
	send({'msg': username + " has joined the chat room: " + room}, 
		room = room)

@socketio.on('leave')
def handle_leave(data):
	username = data['username']
	room = data['room']

	leave_room(room)
	send({'msg': username + " has left the chat room: " + room}, 
		room = room)

if __name__ == "__main__":
	socketio.run(app, debug=True)
