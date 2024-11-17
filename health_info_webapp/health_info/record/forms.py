from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class RecordForm(FlaskForm):
    email = StringField('Public Servant Email', validators=[DataRequired()])
    cname = StringField('Country Name', validators=[DataRequired()])
    disease_code = StringField('Disease Code', validators=[DataRequired()])
    total_deaths = IntegerField('Total Deaths', validators=[DataRequired(), NumberRange(min=0)])
    total_patients = IntegerField('Total Patients', validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField('Submit')