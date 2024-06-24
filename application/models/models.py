from flask_login import UserMixin
from datetime import datetime
from models import db

class User(db.Model, UserMixin):

	__tablename__ = 'users'

	__table_args__ = (
		db.UniqueConstraint('user'),
	)

	id = db.Column(db.Integer, primary_key=True)
	## email
	user = db.Column(db.String(255, collation='utf8mb4_general_ci'), nullable=False)
	## hashed password
	password = db.Column(db.String(255, collation='utf8mb4_general_ci'), nullable=False)
	created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
	updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

	def __init__(self, user, password):
		self.user = user
		self.password = password
