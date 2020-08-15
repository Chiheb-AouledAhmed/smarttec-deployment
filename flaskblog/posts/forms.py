from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.fields.html5 import DateTimeLocalField
from wtforms.validators import DataRequired


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    date = DateTimeLocalField(
        'Date de début de formation', format='%Y-%m-%d'+'T'+'%H:%M')
    zoom_link = StringField('Zoom link', validators=[DataRequired()])
    submit = SubmitField('Post')
