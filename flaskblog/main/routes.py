import hashlib
from flask import render_template, request, Blueprint, url_for, abort, redirect
from flaskblog.models import Post, User
from flaskblog import db, bcrypt
from flask_login import current_user, login_required
from flaskblog.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                                   RequestResetForm, ResetPasswordForm)
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
    if(current_user.is_authenticated)and(current_user.acc_rights != 0):
        abort(403)
    update_form = UpdateAccountForm()
    user = ""
    if(request.method == "POST"):
        if(request.headers["Content-Type"] == "application/json"):
            username = request.json['username']
            user = User.query.filter_by(username=username).first_or_404()
            print(user)
    if update_form.validate_on_submit():
        print(request.form)
        user.username = update_form.username.data
        user.email = update_form.email.data
        db.session.commit()
        return redirect(url_for('main.add_users'))
    form_users = User.query.filter_by(acc_rights=1).all()
    users = User.query.filter_by(acc_rights=2).all()
    return render_template('add_users.html', form_users=form_users, users=users, form=update_form)
    #


@main.route("/payment", methods=['GET', 'POST'])
def payment():
    NumSite = "5"
    Password = "5"
    orderID = "5"
    Currency = "5"
    signature = hashlib.sha1((NumSite+Password+orderID+Currency).encode())
    return render_template('payment.html', NumSite=NumSite, Password=Password, orderID=orderID, Currency=Currency, signature=signature)
