from . import db
from flask.ext.login import UserMixin
from . import login_manager
from werkzeug.security import generate_password_hash, check_password_hash


@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))


class User(UserMixin, db.Model):

	__tablename__ = 'users'

	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(60), unique=True)
	password_hash = db.Column(db.String(128))
	first_name = db.Column(db.String(25))
	last_name = db.Column(db.String(25))
	name = db.Column(db.String(50))
	active = db.Column(db.Boolean, default=1)
	tasks = db.relationship('Task', backref='employee', lazy='dynamic', foreign_keys='Task.assigned_to')
	assignments = db.relationship('Task', backref='assigner', lazy='dynamic', foreign_keys='Task.assigned_by')
	role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
	magazines = db.relationship('Magazine', backref='sales_person', lazy='dynamic')

	@property
	def password(self):
	    raise AttributeError('password is not a readable attribute')

	@password.setter
	def password(self, password):
	    self.password_hash = generate_password_hash(password)

	def verify_password(self, password):
		return check_password_hash(self.password_hash, password)
	

	def __repr__(self):
		return '{}'.format(self.name)


class Role(db.Model):

	__tablename__ = 'roles'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(20))
	permissions = db.Column(db.Integer, default=1)
	users = db.relationship('User', backref='role', lazy='dynamic')


class Client(db.Model):

	__tablename__ = 'clients'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(120))
	owner = db.Column(db.String(60))
	owner_email = db.Column(db.String(60))
	owner_phone = db.Column(db.String(60))
	contact = db.Column(db.String(60))
	email = db.Column(db.String(60))
	phone = db.Column(db.String(25))
	address = db.Column(db.String(100))
	active = db.Column(db.Boolean, default=1)
	note = db.Column(db.Text)
	magazines = db.relationship('Magazine', backref='owner', lazy='dynamic')
	sections = db.relationship('Section', backref='owner', lazy='dynamic')

	def __repr__(self):
		return '{}'.format(self.name)


class Magazine(db.Model):

	__tablename__ = 'magazines'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(120))
	client_mag = db.Column(db.String(120))
	pages = db.Column(db.Integer)
	active = db.Column(db.Boolean, default=1)
	published = db.Column(db.DateTime)
	note = db.Column(db.Text)
	status = db.Column(db.String(40), default='active')
	client_id = db.Column(db.Integer, db.ForeignKey('clients.id'))
	sales_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	sections = db.relationship('Section', backref='magazine', lazy='dynamic')
	

	def __repr__(self):
		return '{}'.format(self.name)


class Section(db.Model):

	__tablename__ = 'sections'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(120))
	mag_section = db.Column(db.String(120))
	description = db.Column(db.Text)
	status = db.Column(db.String(40), default='active')
	active = db.Column(db.Boolean, default=1)
	note = db.Column(db.Text)
	magazine_id = db.Column(db.Integer, db.ForeignKey('magazines.id'))
	client_id = db.Column(db.Integer, db.ForeignKey('clients.id'))
	tasks = db.relationship('Task', backref='section', lazy='dynamic')


class Task(db.Model):
	
	__tablename__ = 'tasks'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50))
	description = db.Column(db.Text)
	create_date = db.Column(db.DateTime)
	due_date = db.Column(db.DateTime)
	status = db.Column(db.String(50))
	note = db.Column(db.Text)
	active = db.Column(db.Boolean, default=1)
	section_id = db.Column(db.Integer, db.ForeignKey('sections.id'))
	assigned_to = db.Column(db.Integer, db.ForeignKey('users.id'))
	assigned_by = db.Column(db.Integer, db.ForeignKey('users.id'))

	def __repr__(self):
		return '{}'.format(self.name)

