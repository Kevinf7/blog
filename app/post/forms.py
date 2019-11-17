from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import InputRequired, Email, Length, Optional

class PostForm(FlaskForm):
    heading = StringField('Title', validators=[InputRequired(), Length(max=100)])
    post = TextAreaField('Write something')
    tags = StringField('Tags')
    submit = SubmitField('Submit')

# Two forms for commeting, one if user is not logged in
class CommentFormAnon(FlaskForm):
    name = StringField('Name', validators=[InputRequired(), Length(max=20)])
    email = StringField('Email', validators=[Length(max=50), Email()])
    comment = TextAreaField('Leave a comment', validators=[InputRequired(), Length(max=200)])
    submit = SubmitField('Submit')
    recaptcha = RecaptchaField()

# Another form if user is logged in
class CommentFormReg(FlaskForm):
    comment = TextAreaField('Leave a comment', validators=[InputRequired(), Length(max=200)])
    submit = SubmitField('Submit')
    recaptcha = RecaptchaField()

class DeletePostForm(FlaskForm):
    submit = SubmitField('Delete')
