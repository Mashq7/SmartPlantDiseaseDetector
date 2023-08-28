from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

spdd_db = SQLAlchemy()


class User(spdd_db.Model):
	id = spdd_db.Column(spdd_db.Integer, primary_key=True)
	username = spdd_db.Column(spdd_db.String(20), unique=True, nullable=False)
	email = spdd_db.Column(spdd_db.String(120), unique=True, nullable=False)
	image_file = spdd_db.Column(spdd_db.String(20), nullable=False, default='default.jpg')
	password = spdd_db.Column(spdd_db.String(60), nullable=False)
	plants = spdd_db.relationship('Plant', backref='author', lazy=True)

	def __repr__(self):
		return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Plant(spdd_db.Model):
	id = spdd_db.Column(spdd_db.Integer, primary_key=True)
	title = spdd_db.Column(spdd_db.String(100), nullable=False)
	image_file = spdd_db.Column(spdd_db.String(20), nullable=False, default='default.jpg')
	accuracy = spdd_db.Column(spdd_db.Float, nullable=False)
	desc = spdd_db.Column(spdd_db.Text, nullable=False)
	proc_date = spdd_db.Column(spdd_db.DateTime, nullable=False, default= datetime.utcnow)
	user_id = spdd_db.Column(spdd_db.Integer, spdd_db.ForeignKey('user.id'), nullable=False)

	def __repr__(self):
		return f"Plant('{self.title}', '{self.accuracy}', '{self.image_file}', '{self.desc}')"