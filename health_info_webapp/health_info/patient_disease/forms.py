from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SubmitField
from wtforms.validators import DataRequired

class PatientDiseaseForm(FlaskForm):
    email = StringField('Patient Email', validators=[DataRequired()])
    disease_code = StringField('Disease Code', validators=[DataRequired()])
    submit = SubmitField('Submit')
