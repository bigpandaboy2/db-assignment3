from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class PublicServantForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(max=60)])
    department = StringField('Department', validators=[DataRequired(), Length(max=50)])
    submit = SubmitField('Submit')