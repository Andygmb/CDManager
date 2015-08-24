from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, TextField, \
SelectField, DateField, IntegerField, TextAreaField, widgets, SubmitField
from wtforms.ext.sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
from wtforms.validators import InputRequired, Email, EqualTo, NumberRange, Optional
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


class MultiCheckboxField(QuerySelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


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


class EditClient(Form):
    name = StringField('Company Name', validators=[InputRequired()])
    address = StringField('Address', validators=[InputRequired()])
    main_phone = StringField('Office Phone')
    note = StringField('Notes')
    submit = SubmitField()


class EditContact(Form):
    first_name = StringField('First Name', validators=[InputRequired()])
    last_name = StringField('Last Name', validators=[InputRequired()])
    position = StringField('Position', validators=[InputRequired()])
    main_email = StringField('Main Email', validators=[InputRequired(), Email()])
    main_phone = StringField('Main Phone', validators=[InputRequired()])
    secondary_email = StringField('Secondary Email', validators=[Optional(), Email()])
    secondary_phone = StringField('Secondary Phone', validators=[Optional()])
    submit = SubmitField()


class EditMag(Form):
    owner = QuerySelectField('Client', query_factory=get_all_clients, get_label='name',
                             validators=[InputRequired()])
    published = SelectField('Published', choices=[('not published', 'Not Published'), ('published', 'Published')])
    name = StringField('Magazine Name', validators=[InputRequired()])
    sales_person = QuerySelectField('Sales Person', query_factory=get_all_sales, get_label='name',
                                    validators=[InputRequired()])
    page_count = IntegerField('Page Count', validators=[InputRequired()])
    note = StringField('Notes')
    submit = SubmitField()


class EditTask(Form):
    employee = QuerySelectField('Assign To', query_factory=get_all_users, get_label='name',
                                validators=[InputRequired()])
    name = StringField('Task Name', validators=[InputRequired()])
    description = StringField('Description')
    due_date = DateField(format='%m/%d/%Y', validators=[Optional()])
    status = SelectField('Status', choices=[('active', 'Active'), ('road-blocked', 'Road Blocked'),
        ('finished', 'Finished'), ('inactive', 'Inactive')], validators=[InputRequired()])
    comment = TextAreaField('Comment (Optional)')
    pages = MultiCheckboxField('Pages', get_label='number')
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