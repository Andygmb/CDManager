from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField,  SubmitField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import InputRequired, Email, EqualTo
from ..models import Client, User, Magazine, Page, Role


def get_all_clients():
    return Client.query.filter_by(active=True).order_by(Client.name).all()


def get_all_magazines():
    return Magazine.query.filter_by(active=True).filter_by(published=None).order_by(Magazine.name).all()


def get_all_pages():
    return Page.query.filter_by(magazine_id=id).all()


def get_all_users():
    return User.query.order_by(User.name).all()


def get_all_sales():
    return User.query.filter_by(role_id=4).order_by(User.name).all()


def get_all_designers():
    return User.query.filter(User.role_id<=3).all()


def get_all_roles():
    return Role.query.all()


class EditUser(Form):
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password',
                             validators=[EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Confirm Password')
    first_name = StringField('First Name', validators=[InputRequired()])
    last_name = StringField('Last Name', validators=[InputRequired()])
    role = QuerySelectField('Role', query_factory=get_all_roles, get_label='name',
                            validators=[InputRequired()])
    submit = SubmitField()


class LogIn(Form):
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Sign In')


class CallLog(Form):
    company = StringField('Company', validators=[InputRequired()])
    person = StringField('Person', validators=[InputRequired()])
    notes = StringField('Notes')
    submit = SubmitField('Submit')
