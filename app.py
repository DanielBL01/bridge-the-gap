from flask import Flask, flash, render_template, redirect, url_for
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

predefined_rooms = ["general", "coding", "co-op"]

db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

@app.route("/", methods=['GET', 'POST'])
def index():
	'''route url_for('index')'''

	registration_form = RegistrationForm()

	# User is processed into database on valid form submit -> redirect to login page
	if registration_form.validate_on_submit():
		username = registration_form.username.data
		password = registration_form.password.data
		
		''' 
		Currently password is in plain text. Let's generate a hash from password.
		The pbkdf2_sha256 module actually applies both salt and iteration as discussed in the README
		'''
		hashed_password = pbkdf2_sha256.hash(password)

		# Save user to database
		user = User(username=username, password=hashed_password)
		db.session.add(user)
		db.session.commit()

		flash('Registered successfully. Please log in.', 'success')
		return redirect(url_for('login'))
		
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

	return render_template('chat.html', username=current_user.username, rooms=predefined_rooms)

@app.route("/logout", methods=['GET'])
def logout():
	
	logout_user()
	flash('You have sucessfully logged out', 'sucess')
	return redirect(url_for('login'))
	
# server 'messsage' event handler
@socketio.on('message')
def handle_message(message):
	print(f'\n{message}\n')
	'''
	The "send" method broadcasts the message to all clients which are connected 
	and the message is passed to the client 'message' event handler
	'''
	send({'msg': message['msg'], 'username': message['username'],
		'time': strftime("%b %d, %I:%M%p", localtime())}, room=message['room'])

@socketio.on('join')
def handle_join(data):
	join_room(data['room'])

	send({'msg': data['username'] + " has joined the chat room: " + data['room']}, 
		room=data['room'])


@socketio.on('leave')
def handle_leave(data):
	leave_room(data['room'])

	send({'msg': data['username'] + " has left the chat room: " + data['room']}, 
		room=data['room'])

if __name__ == "__main__":
	socketio.run(app, debug=True)
