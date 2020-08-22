from app import db
from flask_bcrypt import Bcrypt

import jwt
from datetime import datetime, timedelta

class User(db.Model):
	id =db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(255))
	email = db.Column(db.String(255))
	password = db.Column(db.String(256), nullable=False)
	date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
	#trips = db.relationship('Trip', order_by='Trip.id', cascade='all, delete-orphan')

	def __init__(self, name, email, password):
		self.name = name
		self.email = email		
		self.password = Bcrypt().generate_password_hash(password)

	def password_is_valid(self, password):
		return Bcrypt().check_password_hash(self.password, password)

	def save(self):
		db.session.add(self)
		db.session.commit()

	def generate_token(self, user_id):
		try:
			payload = {
				'exp': datetime.utcnow() + timedelta(minutes=5),
				'iat': datetime.utcnow(),
				'sub': user_id
			}
			jwt_string = jwt.encode(
				payload,
				current_app.config.get('SECRET'),
				algorithm='HS256'
				)
			return jwt_string
		except Exception as e:
			print(str(e))
			return None

	@staticmethod
	def decode_token(token):
		try:
			payload = jwt.decode(token, current_app.config.get('SECRET'))
			return payload['sub']
		except jwt.ExpiredSignatureError:
			return 'Token expired'
		except jwt.InvalidTokenError:
			return 'Invalid token'

	@staticmethod
	def get_all():
		return User.query.all()

	def delete(self):
		db.session.delete(self)
		db.session.commit()

	def __repr__(self):
		return '<User: {} {}>'.format(self.name, self.email)

class Trip(db.Model):
	id =db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(255))
	description = db.Column(db.String)
	date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
	date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
		onupdate=db.func.current_timestamp())
	date_starts = db.Column(db.DateTime)
	date_ends = db.Column(db.DateTime)
	owner = db.Column(db.Integer)#, db.ForeignKey(User.id))

	def __init__(self, name, description, 
			date_starts, date_ends, owner):
		self.name = name
		self.description = description
		self.date_starts = date_starts
		self.date_ends = date_ends
		self.owner = owner
	
	def save(self):
		db.session.add(self)
		db.session.commit()

	@staticmethod
	def get_all():
		return Trip.query.all()#filter_by(owner=user_id)

	def delete(self):
		db.session.delete(self)
		db.session.commit()
	
	def __repr__(self):
		return '<Trip: {}>'.format(self.name)

