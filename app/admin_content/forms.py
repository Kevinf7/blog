from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField

class ContentManageForm(FlaskForm):
    #post is actually content, just call it post because tinymce uses post id selector
    post = TextAreaField('Write something')
    submit = SubmitField('Submit')
