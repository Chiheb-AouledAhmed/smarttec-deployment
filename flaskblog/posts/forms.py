from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, IntegerField, HiddenField, SelectField
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
    theme = SelectField('Thème de la formation', coerce=int)
    images = StringField(
        'Images de la description de la scéance (Max: 3 par Scéance)')
    submit = SubmitField('Post')


class SceanceForm(FlaskForm):
    title = StringField('Titre', validators=[DataRequired()])
    content = TextAreaField('Description', validators=[DataRequired()])
    date = DateTimeLocalField(
        'Date de début de formation', format='%Y-%m-%d'+'T'+'%H:%M')
    document = StringField('Lien du document')
    zoom_video = StringField('Lien de la vidéo zoom')
    submit = SubmitField('Mettre à jour')


class DocumentForm(FlaskForm):
    title = StringField('Titre', validators=[DataRequired()])
    url = StringField('Document URL', validators=[DataRequired()])
    submit = SubmitField('Ajouter le document')


class DeleteImageForm(FlaskForm):
    image_id = HiddenField("image_id")
    submit = SubmitField('Mettre à jour')


class DeleteDocumentForm(FlaskForm):
    document_id = HiddenField("document_id")
    submit = SubmitField('Supprimer')


class DeleteThemeForm(FlaskForm):
    theme_id = HiddenField("theme_id")
    submit = SubmitField('Mettre à jour')


class FileForm(FlaskForm):
    file = StringField('Ajouter le lien du fichier')
    submit = SubmitField('Post')


class CertificateForm(FlaskForm):
    cert_id = HiddenField("cert_id")
    ref = StringField('Référence du certificat',
                      validators=[DataRequired()])
    score = IntegerField('Score',
                         validators=[DataRequired()])
    submit = SubmitField('Chercher le certificat')


class SubForm(FlaskForm):
    sub_id = HiddenField("sub_id")
    mode = SelectField('Type de Désactivation', choices=[
        ('1', 'Désactivation temporaire'), ('2', 'Désactivation permanente'), ('3', 'Réactivation')])
    submit = SubmitField()


class PaymentMethodForm(FlaskForm):
    mode_de_paiement = SelectField('Mode de paiement', choices=[
        ('MoneyGram', 'MoneyGram'), ('Western Union', 'Western Union'), ('Virement Bancaire', 'Virement Bancaire'), ('Paypal', 'Paypal')])
    submit = SubmitField('Mettre à jour')


class ThemeForm(FlaskForm):
    theme_id = HiddenField("theme_id")
    name = StringField('Nom du thème', validators=[DataRequired()])
    url = StringField('Lien de l''image du thème', validators=[DataRequired()])
    submit = SubmitField('Ajouter le thème')
