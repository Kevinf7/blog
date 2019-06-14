from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import InputRequired, Email, Length

class ContactForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired(), Length(max=20)])
    email = StringField('Email', validators=[InputRequired(), Email(), Length(max=50)])
    message = TextAreaField('Leave a message', validators=[InputRequired(), Length(max=400)])
    submit = SubmitField('Submit')
    recaptcha = RecaptchaField()
