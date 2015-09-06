from flask_wtf import Form
from wtforms import StringField, SelectField, IntegerField, SubmitField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import InputRequired
from ..models import Client, User


def get_all_clients():
    return Client.query.filter_by(active=True).order_by(Client.name).all()


def get_all_sales():
    return User.query.filter_by(role_id=4).order_by(User.name).all()


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
