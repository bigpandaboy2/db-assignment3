from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length

class DiseaseForm(FlaskForm):
    disease_code = StringField('Disease Code', validators=[DataRequired(), Length(max=50)])
    pathogen = StringField('Pathogen', validators=[DataRequired(), Length(max=20)])
    description = TextAreaField('Description', validators=[Length(max=140)])
    disease_type_id = IntegerField('Disease Type ID', validators=[DataRequired()])
    submit = SubmitField('Submit')