from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
	'''
	Database for Users

	Each user will have a primary key with a non-empty unique username 
	with a 20 character limit. A user must also have a password with a
	20 character limit that is non-empty but can be non-unique.

	Flask will use the lowercase Class name as the database name

	PostgreSQL has 'user' as a reserved word so I'll name it 'users'
	'''
	
	__tablename__ = 'users'
	
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	password = db.Column(db.String(20), unique=False, nullable=False)

	
