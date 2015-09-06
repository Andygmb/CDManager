from flask_wtf import Form
from wtforms import StringField, SelectField, DateField, TextAreaField, widgets, SubmitField
from wtforms.ext.sqlalchemy.fields import QuerySelectMultipleField
from wtforms.validators import InputRequired, Optional
from ..models import User


def get_all_users():
    return User.query.order_by(User.name).all()


class MultiCheckboxField(QuerySelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class EditTask(Form):
    users = MultiCheckboxField('Assign To', query_factory=get_all_users, get_label='name',
                               validators=[InputRequired()])
    name = StringField('Task Name', validators=[InputRequired()])
    description = StringField('Description')
    due_date = DateField(format='%m/%d/%Y', validators=[Optional()])
    status = SelectField('Status', choices=[('active', 'Active'), ('road-blocked', 'Road Blocked'),
                                            ('finished', 'Finished'), ('inactive', 'Inactive')],
                         validators=[InputRequired()])
    comment = TextAreaField('Comment (Optional)')
    pages = MultiCheckboxField('Pages', get_label='number')
    submit = SubmitField()
