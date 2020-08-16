from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from flask_wtf.file import FileField, FileAllowed
from wtforms.fields.html5 import DateTimeLocalField
from wtforms.validators import DataRequired


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    date = DateTimeLocalField(
        'Date de début de formation', format='%Y-%m-%d'+'T'+'%H:%M')
    zoom_link = StringField('Zoom link', validators=[DataRequired()])
    submit = SubmitField('Post')


class SceanceForm(FlaskForm):
    title = StringField('Titre', validators=[DataRequired()])
    content = TextAreaField('Description', validators=[DataRequired()])
    date = DateTimeLocalField(
        'Date de début de formation', format='%Y-%m-%d'+'T'+'%H:%M')
    document = FileField('Ajouter un document', validators=[
        FileAllowed(['pdf', 'doc', 'docx', 'pptx', 'ppt', 'xlsx', 'csv'])])
    submit = SubmitField('Mettre à jour')
