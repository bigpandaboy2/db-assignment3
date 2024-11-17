from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SubmitField
from wtforms.validators import DataRequired

class DiscoverForm(FlaskForm):
    cname = StringField('Country Name', validators=[DataRequired()])
    disease_code = StringField('Disease Code', validators=[DataRequired()])
    first_enc_date = DateField('First Encounter Date', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Submit')
