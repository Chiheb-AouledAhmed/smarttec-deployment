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
    date_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    start_date = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)
    zoom_link = db.Column(db.String(200))
    theme = db.Column(db.String(20), default="theme 1")
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    subscriptions = db.relationship(
        'Subscription', backref='subscribers', lazy=True)
    sceances = db.relationship(
        'Sceance', backref='session', lazy=True)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


class Subscription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
    Test_score = db.Column(db.Integer)
    Certif_ref = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

    def __repr__(self):
        return f"Subscription('{self.id}', '{self.date_posted}')"


class Sceance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    num = db.Column(db.Integer, nullable=False)
    session_id = db.Column(
        db.Integer, db.ForeignKey('post.id'), nullable=False)
    documents = db.relationship('Document', backref='sceance.id', lazy=True)

    def __repr__(self):
        return f"Sceance('{self.id}', '{self.num}')"


class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start = db.Column(db.DateTime, nullable=False)
    end = db.Column(db.DateTime, nullable=False)
    url = db.Column(db.String(200), nullable=False)
    sceance = db.Column(db.Integer, db.ForeignKey(
        'sceance.id'), nullable=False)

    def __repr__(self):
        return f"Document('{self.id}', '{self.url}')"


class Userinfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Nom = db.Column(db.String(30), nullable=False)
    Prenom = db.Column(db.String(30), nullable=False)
    Sexe = db.Column(db.String(20), nullable=False)
    Num_tel = db.Column(db.String(20), nullable=False)
    Pays = db.Column(db.String(20), nullable=False)
    Niv_etude = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f"Userinfo('{self.Nom}', '{self.Prenom}')"
