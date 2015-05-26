from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, TextField, \
SelectField, DateField, IntegerField, SubmitField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import InputRequired, Email, EqualTo
from models import Client, User, Magazine


def get_all_clients():
	return Client.query.all()

def get_all_magazines():
	return Magazine.query.filter_by(active=True).filter_by(published=None).all()

def get_all_users():
	return User.query.all()


class EditUser(Form):
	email = StringField('Email', validators=[InputRequired(), Email()])
	password = PasswordField('Password', \
		validators=[EqualTo('confirm', message='Passwords must match')])
	confirm = PasswordField('Confirm Password')
	first_name = StringField('First Name', validators=[InputRequired()])
	last_name = StringField('Last Name', validators=[InputRequired()])
	submit = SubmitField()

class EditClient(Form):
	name = StringField('Company Name', validators=[InputRequired()])
	address = StringField('Address', validators=[InputRequired()])
	contact = StringField('Contact', validators=[InputRequired()])
	email = StringField('Email', validators=[InputRequired(), Email()])
	phone = StringField('Phone', validators=[InputRequired()])
	note =TextField('Notes')
	submit = SubmitField()

class EditMag(Form):
	owner = QuerySelectField('Client', query_factory=get_all_clients, get_label='name', 
		validators=[InputRequired()])
	published = SelectField('Published', choices=[('not published', 'Not Published'), ('published', 'Published')])
	name = StringField('Magazine Name', validators=[InputRequired()])
	sales_person = StringField('Sales Person', validators=[InputRequired()])
	pages = IntegerField('Page Count', validators=[InputRequired()])
	note = TextField('Notes')
	submit = SubmitField()

class EditTask(Form):
	magazine = QuerySelectField('Magazine', query_factory=get_all_magazines, get_label='client_mag', 
		validators=[InputRequired()])
	status = SelectField('Status', choices=[('active', 'Active'), ('road-blocked', 'Road Blocked'), \
		('finished', 'Finished'), ('inactive', 'Inactive')], validators=[InputRequired()])
	employee = QuerySelectField('Assign To', query_factory=get_all_users, get_label='name', 
		validators=[InputRequired()])
	name = StringField('Task Name', validators=[InputRequired()])
	description = TextField('Description', validators=[InputRequired()])
	due_date = DateField(format='%m/%d/%Y')
	note = TextField('Notes')
	submit = SubmitField()

class LogIn(Form):
	email = StringField('Email', validators=[InputRequired(), Email()])
	password = PasswordField('Password', validators=[InputRequired()])
	remember_me = BooleanField('Keep me logged in')
	submit = SubmitField('Sign In')