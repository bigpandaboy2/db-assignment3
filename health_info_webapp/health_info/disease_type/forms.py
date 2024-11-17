from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange

class DiseaseTypeForm(FlaskForm):
    id = IntegerField('ID', validators=[DataRequired(), NumberRange(min=1)])
    description = StringField('Description', validators=[DataRequired(), Length(max=140)])
    submit = SubmitField('Submit')