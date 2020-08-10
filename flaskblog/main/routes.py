import hashlib
from flask import render_template, request, Blueprint, url_for, abort, redirect
from flaskblog.models import Post, User
from flaskblog import db, bcrypt
from flask_login import current_user, login_required
from flaskblog.users.forms import *
main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
    """
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(
        Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts)
    """
    if(current_user.is_authenticated):
        print(current_user.acc_rights)
    return render_template('index.html', title="Home Page", cur_user=current_user)


@main.route("/about")
def about():
    return render_template('about.html', title='About')


@main.route("/add_users", methods=['GET', 'POST'])
def add_users():
    if(not(current_user.is_authenticated) or (current_user.acc_rights != 0)):
        abort(403)
    update_form = UpdateAccountForm()
    delete_form = DeleteAccountForm()
    add_form = RegistrationForm()
    form_users = User.query.filter_by(acc_rights=1).all()
    users = User.query.filter_by(acc_rights=2).all()
    return render_template('add_users.html', form_users=form_users,
                           users=users, update_form=update_form, add_form=add_form, delete_form=delete_form)
