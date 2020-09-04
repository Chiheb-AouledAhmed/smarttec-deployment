from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, HiddenField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from flaskblog.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
    acc_rights = HiddenField()

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                'That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(
                'That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[
                        FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')
    password = PasswordField('New Password')
    this_user = HiddenField('this_user')

    def validate_username(self, username):
        if(self.this_user.data):
            cur_user = User.query.filter_by(
                username=self.this_user.data).first()
        else:
            cur_user = current_user
        if username.data != cur_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError(
                    'That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if(self.this_user.data):
            cur_user = User.query.filter_by(
                username=self.this_user.data).first()
        else:
            cur_user = current_user
        if email.data != cur_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError(
                    'That email is taken. Please choose a different one.')


class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError(
                'There is no account with that email. You must register first.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')


class DeleteAccountForm(FlaskForm):
    this_user = HiddenField('this_user')
    submit = SubmitField('Delete')


class InfoForm(FlaskForm):
    Nom = StringField('Nom', validators=[DataRequired()])
    Prenom = StringField('Prénom', validators=[DataRequired()])
    Sexe = SelectField('Sexe', choices=[
                       ('male', 'Male'), ('female', 'Female')])
    Num_tel = StringField('Numéro de téléphone/ WhatsApp',
                          validators=[DataRequired()])
    Pays = StringField('Pays', validators=[DataRequired()])
    Niv_etude = StringField('Niveau d''étude / profession',
                            validators=[DataRequired()])
    submit = SubmitField('Submit')
