from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, IntegerField
from flask_wtf.file import FileField, FileAllowed
from wtforms.fields.html5 import DateTimeLocalField
from wtforms.validators import DataRequired, Length


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=50)])
    description = TextAreaField('Description', validators=[
                                DataRequired(), Length(max=200)])
    content = TextAreaField('Contenu', validators=[DataRequired()])
    youtube_url = StringField(
        'Lien Youtube de la vidéo', validators=[DataRequired()])
    price = IntegerField('Prix de la Session (en euro)',
                         validators=[DataRequired()])
    num_posts = IntegerField('Nombre de sceances',
                             validators=[DataRequired()])
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
