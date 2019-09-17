from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField
from wtforms.validators import InputRequired


class SearchForm(FlaskForm):
    min_bedrooms = IntegerField('Minimum Bedrooms', validators=[InputRequired()])
    max_bedrooms = IntegerField('Maximum Bedrooms', validators=[InputRequired()])
    postcode = IntegerField('Postcode', validators=[InputRequired()])
    submit = SubmitField('Submit')
