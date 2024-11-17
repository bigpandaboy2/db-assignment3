from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange

class CountryForm(FlaskForm):
    cname = StringField('Country Name', validators=[DataRequired(), Length(max=50)])
    population = IntegerField('Population', validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField('Submit')