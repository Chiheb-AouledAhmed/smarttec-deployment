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
    if(request.method == 'POST'):
        print(request.json)
    """
    if update_form.data and update_form.validate():
        #print(request.form)
        username=update_form.this_user.data
        user = User.query.filter_by(username=username).first()
        for attr in ['username','email','password']:
            if(update_form.username.data):
                user.username=update_form.username.data
            if(update_form.email.data):
                user.email=update_form.email.data
            if(update_form.password.data):
                user.password=update_form.password.data
        db.session.commit()
        return redirect(url_for('main.add_users'))
    if delete_form.data and delete_form.validate():
        #print(request.form)
        username=delete_form.this_user.data
        user = User.query.filter_by(username=username).first()
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for('main.add_users'))
    if add_form.data and add_form.validate():
        hashed_password = bcrypt.generate_password_hash(
            add_form.password.data).decode('utf-8')
        user = User(username=add_form.username.data,
                    email=add_form.email.data, password=hashed_password,acc_rights=add_form.acc_rights.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('main.add_users'))
    """
    """
    if(request.method == "GET"):
        errors = request.args.getlist('errors')
        print(errors)
    if(not(errors)):
        errors = []
    """

    form_users = User.query.filter_by(acc_rights=1).all()
    users = User.query.filter_by(acc_rights=2).all()
    return render_template('add_users.html', form_users=form_users, users=users, update_form=update_form, add_form=add_form, delete_form=delete_form)
    #


@main.route("/payment", methods=['GET', 'POST'])
def payment():
    NumSite = "5"
    Password = "5"
    orderID = "5"
    Currency = "5"
    signature = hashlib.sha1((NumSite+Password+orderID+Currency).encode())
    return render_template('payment.html', NumSite=NumSite, Password=Password, orderID=orderID, Currency=Currency, signature=signature)
