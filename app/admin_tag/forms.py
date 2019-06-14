from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired, Length

class EditTagForm(FlaskForm):
    tag_name = StringField('Tag Name', validators=[InputRequired(), Length(max=20)])
    submit = SubmitField('Submit')

class DeleteTagForm(FlaskForm):
    submit = SubmitField('Delete')
