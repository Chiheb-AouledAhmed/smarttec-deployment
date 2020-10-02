from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flaskblog import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False,
                           default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    acc_rights = db.Column(db.Integer, default=2)
    posts = db.relationship('Post', backref='author', lazy=True)
    subscriptions = db.relationship(
        'Subscription', backref='subscribed', lazy=True)
    infos = db.relationship(
        'Userinfo', backref='currentuser', lazy=True)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    youtube_url = db.Column(db.Text, nullable=True)
    num_posts = db.Column(db.Integer, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    start_date = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)
    zoom_link = db.Column(db.Text)
    theme = db.Column(db.Integer, db.ForeignKey('theme.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    images = db.relationship('PostImage', backref='post', lazy=True)
    subscriptions = db.relationship(
        'Subscription', backref='subscribers', lazy=True)
    sceances = db.relationship(
        'Sceance', backref='session', lazy=True)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


class Subscription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Test_score = db.Column(db.Integer)
    Certif_ref = db.Column(db.Integer)
    date_posted = date_certif = db.Column(db.DateTime, nullable=False,
                                          default=datetime.utcnow)
    date_certif = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    payment_method = db.Column(db.String(20), nullable=False)
    status = db.Column(db.Integer, default=1)

    def __repr__(self):
        return f"Subscription('{self.id}', '{self.date_posted}')"


class Sceance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    num = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=True)
    start_date = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)
    session_id = db.Column(
        db.Integer, db.ForeignKey('post.id'), nullable=False)
    zoom_video = db.Column(db.Text, nullable=True)
    documents = db.relationship('Document', backref='sceance.id', lazy=False)

    def __repr__(self):
        return f"Sceance('{self.id}', '{self.num}')"


class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.Text, nullable=False)
    sceance = db.Column(db.Integer, db.ForeignKey(
        'sceance.id'), nullable=False)

    def __repr__(self):
        return f"Document('{self.id}', '{self.url}')"


class PostImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.Text, nullable=False)
    ima_post = db.Column(db.Integer, db.ForeignKey(
        'post.id'), nullable=False)

    def __repr__(self):
        return f"Image('{self.id}', '{self.url}')"


class Userinfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Nom = db.Column(db.String(30), nullable=True)
    Prenom = db.Column(db.String(30), nullable=True)
    Sexe = db.Column(db.String(20), nullable=True)
    Num_tel = db.Column(db.String(20), nullable=True)
    Pays = db.Column(db.String(20), nullable=True)
    Niv_etude = db.Column(db.String(20), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.id'), nullable=False)

    def __repr__(self):
        return f"Userinfo('{self.Nom}', '{self.Prenom}')"


class Theme(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=True)
    url = db.Column(db.Text, nullable=False)
    theme_posts = db.relationship('Post', backref='post_theme', lazy=False)

    def __repr__(self):
        return f"Image('{self.id}', '{self.url}')"
