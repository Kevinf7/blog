from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import InputRequired, Email, EqualTo, ValidationError, Length
from flask_login import UserMixin
from app.models import User

# usermixin provides some handy functions for user class
class LoginForm(FlaskForm, UserMixin):
    email = StringField('Email', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email()])
    firstname = StringField('First Name', validators=[InputRequired(), Length(max=20)])
    lastname = StringField('Last Name', validators=[InputRequired(), Length(max=50)])
    password = PasswordField('Password', validators=[InputRequired()])
    password2 = PasswordField('Repeat Password', validators=[InputRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    # wtforms takes validate_<field_name> as custom validators
    # so the below validator gets invoked on username
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Email has previously registered')

class PostForm(FlaskForm):
    heading = StringField('Title', validators=[InputRequired(), Length(max=100)])
    post = TextAreaField('Write something')
    tags = StringField('Tags')
    submit = SubmitField('Submit')

class CommentFormAnon(FlaskForm):
    name = StringField('Name', validators=[InputRequired(), Length(max=20)])
    email = StringField('Email', validators=[Length(max=50)])
    comment = TextAreaField('Leave a comment', validators=[InputRequired(), Length(max=200)])
    submit = SubmitField('Submit')

class CommentFormReg(FlaskForm):
    comment = TextAreaField('Leave a comment', validators=[InputRequired(), Length(max=200)])
    submit = SubmitField('Submit')

class ContactForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired(), Length(max=20)])
    email = StringField('Email', validators=[InputRequired(), Email(), Length(max=50)])
    message = TextAreaField('Leave a message', validators=[InputRequired(), Length(max=400)])
    submit = SubmitField('Submit')

class DeletePostForm(FlaskForm):
    submit = SubmitField('Submit')

class EditTagForm(FlaskForm):
    tag_name = StringField('Tag Name', validators=[InputRequired(), Length(max=20)])
    submit = SubmitField('Submit')

class DeleteTagForm(FlaskForm):
    submit = SubmitField('Delete')

class ForgotPasswordForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email()])
    submit = SubmitField('Submit')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Enter new password', validators=[InputRequired()])
    password2 = PasswordField(
        'Repeat password', validators=[InputRequired(), EqualTo('password')])
    submit = SubmitField('Submit')
