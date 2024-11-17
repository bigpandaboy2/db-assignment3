from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Email, NumberRange

class UserForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    name = StringField('Name', validators=[DataRequired()])
    surname = StringField('Surname', validators=[DataRequired()])
    salary = IntegerField('Salary', validators=[DataRequired(), NumberRange(min=0)])
    phone = StringField('Phone', validators=[DataRequired()])
    cname = StringField('Country Name', validators=[DataRequired()])
    submit = SubmitField('Submit')