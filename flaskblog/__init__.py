from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flaskblog.config import Config
from flask_migrate import Migrate

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()


def create_app(config_class=Config):
    app = Flask(
        __name__, template_folder="templates/startbootstrap-sb-admin-2-gh-pages")
    app.config.from_object(Config)
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    migrate = Migrate(app, db)
    from flaskblog.users.routes import users
    from flaskblog.posts.routes import posts
    from flaskblog.main.routes import main
    from flaskblog.transactions.routes import trans
    from flaskblog.errors.handlers import errors
    from flaskblog.models import User, Post, Subscription, Sceance, PostImage, Document, Userinfo, Theme
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)
    app.register_blueprint(trans)

    with app.app_context():
        """
        db.drop_all()
        db.create_all()
        pwd = bcrypt.generate_password_hash(
            "admin123").decode('utf-8')
        admin_user = User(username="admin",
                          email="adminadmin@admin.com", password=pwd, acc_rights=0)
        default_theme = Theme(
            name="no theme", url="https://vennexgroup.ch/storage/Clientes/VennexGroupSAS/Portal/imagenes/contenidos/13927-vennex404.svg")
        db.session.add(default_theme)
        db.session.add(admin_user)
        db.session.commit()
        """
    return app
