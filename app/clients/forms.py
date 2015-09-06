from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired, Email, Optional

class EditClient(Form):
    name = StringField('Company Name', validators=[InputRequired()])
    address = StringField('Address', validators=[InputRequired()])
    phone = StringField('Office Phone')
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