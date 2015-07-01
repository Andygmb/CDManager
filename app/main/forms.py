from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, TextField, \
SelectField, DateField, IntegerField, TextAreaField, widgets, SubmitField
from wtforms.ext.sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
from wtforms.validators import InputRequired, Email, EqualTo, NumberRange, Optional
from ..models import Client, User, Magazine, Page, Role


def get_all_clients():
    return Client.query.all()

def get_all_magazines():
    return Magazine.query.filter_by(active=True).filter_by(published=None).all()

def get_all_pages():
    return Page.query.filter_by(magazine_id=id).all()

def get_all_users():
    return User.query.all()

def get_all_sales():
    return User.query.filter_by(role_id=4).all()

def get_all_designers():
    return User.query.filter(User.role_id<=3).all()

def get_all_roles():
    return Role.query.all()

class MultiCheckboxField(QuerySelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


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


class EditTask(Form):
    employee = QuerySelectField('Assign To', query_factory=get_all_designers, get_label='name', 
        validators=[InputRequired()])
    name = StringField('Task Name', validators=[InputRequired()])
    description = TextField('Description')
    due_date = DateField(format='%m/%d/%Y')
    status = SelectField('Status', choices=[('active', 'Active'), ('road-blocked', 'Road Blocked'), \
        ('finished', 'Finished'), ('inactive', 'Inactive')], validators=[InputRequired()])
    note = TextAreaField('Notes')
    pages = MultiCheckboxField('Pages', get_label='number')
    submit = SubmitField()


class LogIn(Form):
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Sign In')

class SetPage(Form):
    magazine = QuerySelectField()