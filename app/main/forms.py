from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, TextField, \
SelectField, DateField, IntegerField, SubmitField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import InputRequired, Email, EqualTo, Optional
from ..models import Client, User, Magazine, Section, Role


def get_all_clients():
	return Client.query.all()

def get_all_magazines():
	return Magazine.query.filter_by(active=True).filter_by(published=None).all()

def get_all_sections():
	return Section.query.filter_by(active=True).all()

def get_all_users():
	return User.query.all()

def get_all_sales():
	return User.query.filter_by(role_id=3).all()

def get_all_designers():
	return User.query.filter_by(role_id=2).all()

def get_all_roles():
	return Role.query.all()


class EditUser(Form):
	email = StringField('Email', validators=[InputRequired(), Email()])
	password = PasswordField('Password', \
		validators=[EqualTo('confirm', message='Passwords must match')])
	confirm = PasswordField('Confirm Password')
	first_name = StringField('First Name', validators=[InputRequired()])
	last_name = StringField('Last Name', validators=[InputRequired()])
	role = QuerySelectField('Role', query_factory=get_all_roles, get_label='name',
		validators=[InputRequired()])
	submit = SubmitField()

class EditClient(Form):
	name = StringField('Company Name', validators=[InputRequired()])
	owner = StringField('Owner', validators=[InputRequired()])
	owner_email = StringField('Owner\'s Email', validators=[InputRequired(), Email()])
	owner_phone = StringField('Phone', validators=[InputRequired()])
	contact = StringField('Contact (if not the owner)', validators=[Optional()])
	email = StringField('Email (if not the owner)', validators=[Optional(), Email()])
	phone = StringField('Phone (if not the owner)', validators=[Optional()])
	address = StringField('Address', validators=[InputRequired()])
	note = TextField('Notes')
	submit = SubmitField()

class EditMag(Form):
	owner = QuerySelectField('Client', query_factory=get_all_clients, get_label='name', 
		validators=[InputRequired()])
	published = SelectField('Published', choices=[('not published', 'Not Published'), ('published', 'Published')])
	name = StringField('Magazine Name', validators=[InputRequired()])
	sales_person = QuerySelectField('Sales Person', query_factory=get_all_sales, get_label='name', 
		validators=[InputRequired()])
	pages = IntegerField('Page Count', validators=[InputRequired()])
	note = TextField('Notes')
	submit = SubmitField()

class EditSection(Form):
	magazine = QuerySelectField('Magazine', query_factory=get_all_magazines, get_label='client_mag', 
		validators=[InputRequired()])
	client = QuerySelectField('Client', query_factory=get_all_clients, get_label='name', 
		validators=[InputRequired()])
	name = StringField('Section Name', validators=[InputRequired()])
	description = StringField('Section Description')
	note = TextField('Notes')
	submit = SubmitField()

class EditTask(Form):
	section = QuerySelectField('Section', query_factory=get_all_sections, get_label='mag_section', 
		validators=[InputRequired()])
	status = SelectField('Status', choices=[('active', 'Active'), ('road-blocked', 'Road Blocked'), \
		('finished', 'Finished'), ('inactive', 'Inactive')], validators=[InputRequired()])
	employee = QuerySelectField('Assign To', query_factory=get_all_designers, get_label='name', 
		validators=[InputRequired()])
	name = StringField('Task Name', validators=[InputRequired()])
	description = TextField('Description')
	due_date = DateField(format='%m/%d/%Y')
	note = TextField('Notes')
	submit = SubmitField()

class LogIn(Form):
	email = StringField('Email', validators=[InputRequired(), Email()])
	password = PasswordField('Password', validators=[InputRequired()])
	remember_me = BooleanField('Keep me logged in')
	submit = SubmitField('Sign In')