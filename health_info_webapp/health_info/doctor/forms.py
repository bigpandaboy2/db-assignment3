from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class DoctorForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(max=60)])
    degree = StringField('Degree', validators=[DataRequired(), Length(max=20)])
    submit = SubmitField('Submit')

class SpecializeForm(FlaskForm):
    disease_type_id = StringField('Disease Type ID', validators=[DataRequired()])
    submit = SubmitField('Add Specialization')
