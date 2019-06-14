from flask_wtf import FlaskForm
from wtforms import SubmitField

class DeleteImageForm(FlaskForm):
    submit = SubmitField('Delete')
