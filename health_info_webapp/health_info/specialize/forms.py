from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class SpecializeForm(FlaskForm):
    id = IntegerField('Disease Type ID', validators=[DataRequired(), NumberRange(min=1)])
    email = StringField('Doctor Email', validators=[DataRequired()])
    submit = SubmitField('Submit')