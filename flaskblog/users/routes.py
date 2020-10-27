from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog import db, bcrypt
from flaskblog.models import *
from flaskblog.users.forms import *
from flaskblog.users.utils import save_picture, send_reset_email
from datetime import timedelta
users = Blueprint('users', __name__)


@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(username=form.username.data,
                    email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)


@ users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@ users.route("/logout")
def logout():
    logout_user()
    # flash('An email has been sent with instructions to reset your password.', 'info')
    return redirect(url_for('main.home'))


@ users.route("/mesformations")
@ login_required
def mesformations_catalogue():
    post_ids = [sub.post_id for sub in Subscription.query.filter_by(
        user_id=current_user.id)]

    posts = [Post.query.get(post_id) for post_id in post_ids]
    return render_template('mesFormations_catalogue.html', posts=posts)


@ users.route("/mesformations/<int:post_id>")
@ login_required
def mesformations(post_id):
    post = Post.query.get(post_id)
    subs = Subscription.query.filter_by(user_id=current_user.id).all()
    test = False
    scs = []
    for i in range(1, post.num_posts+1):
        for sc in post.sceances:
            if(sc.num == i):
                scs.append(sc)
                break
    for sub in subs:
        # print("sub {}".format(sub))
        if(sub.post_id == post_id):
            if(sub.status == 1):
                test = True
            else:
                test = False
    sceances = []
    for sc in post.sceances:
        sceances.append((
            (((sc.start_date-datetime.now()) <= timedelta(days=1)) and (test)), sc))
    # print(sceances)
    return render_template('mesFormations.html', current_user=current_user, post=post, test=test, sceances=sceances, scs=scs)


@ users.route("/profile", methods=['GET', 'POST'])
def profile_ano():
    name = request.form.get('search')
    user = User.query.filter_by(username=name).first()
    if(user):
        return redirect(url_for('users.profile', user_id=user.id))
    return render_template('usernotfound.html')


@ users.route("/profile/<int:user_id>", methods=['GET', 'POST'])
@ login_required
def profile(user_id):
    user = User.query.get(user_id)
    if(len(user.infos)):
        userinfo = user.infos[0]
    else:
        userinfo = None
    return render_template('profile.html', user=user, userinfo=userinfo)


@ users.route("/account", methods=['GET', 'POST'])
@ login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for(
        'static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)


@ users.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).order_by(
        Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('user_posts.html', posts=posts, user=user)


@ users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@ users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)


@ users.route("/add/<default_url>", methods=['GET', 'POST'])
def add_user(default_url):
    add_form = RegistrationForm()
    if(not(add_form.acc_rights.data)):
        add_form.acc_rights.data = 2
    if(add_form.validate_on_submit()):
        hashed_password = bcrypt.generate_password_hash(
            add_form.password.data).decode('utf-8')
        user = User(username=add_form.username.data,
                    email=add_form.email.data, password=hashed_password, acc_rights=add_form.acc_rights.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for(default_url))
    messages = []
    for field, errors in add_form.errors.items():
        messages.append(((', '.join(errors))))
    for message in messages:
        flash(message, 'danger')
    return redirect(url_for(default_url))


@ users.route("/delete/<default_url>", methods=['GET', 'POST'])
def delete_user(default_url):
    delete_form = DeleteAccountForm()
    if(delete_form.validate_on_submit()):
        username = delete_form.this_user.data
        print(username)
        user = User.query.filter_by(username=username).first()
        if(user):
            db.session.delete(user)
            db.session.commit()
            flash("username "+username+" successfully deleted", 'success')
        else:
            flash("username not found", 'danger')
        return redirect(url_for(default_url))
    messages = []
    for field, errors in delete_form.errors.items():
        messages.append((field+" : "+(', '.join(errors))))
    for message in messages:
        flash(message, 'danger')
    return redirect(url_for(default_url))


@ users.route("/infos", methods=['GET', 'POST'])
def infos():
    if not(current_user.is_authenticated):
        flash('Login to access this page', 'danger')
        return redirect(url_for('main.home'))
    userinfo = current_user.infos
    form = InfoForm()
    if(request.method == 'POST'):
        if(form.validate_on_submit):
            if(len(userinfo)):
                userinfo[0].Nom = form.Nom.data
                userinfo[0].user_id = current_user.id
                userinfo[0].Prenom = form.Prenom.data
                userinfo[0].Sexe = form.Sexe.data
                userinfo[0].Num_tel = form.Num_tel.data
                userinfo[0].Pays = form.Pays.data
                userinfo[0].Niv_etude = form.Niv_etude.data
            else:
                userinfo = Userinfo(Nom=form.Nom.data, user_id=current_user.id,
                                    Prenom=form.Prenom.data, Sexe=form.Sexe.data,
                                    Num_tel=form.Num_tel.data, Pays=form.Pays.data, Niv_etude=form.Niv_etude.data)
                db.session.add(userinfo)
            db.session.commit()
            flash('sucessfully updated user info', 'success')
            return redirect(url_for('main.home'))
    return render_template('infos_perso.html', form=form, userinfo=userinfo)


@ users.route("/modify/<default_url>", methods=['GET', 'POST'])
def modify_user(default_url):
    update_form = UpdateAccountForm()
    if(update_form.validate_on_submit()):
        username = update_form.this_user.data
        user = User.query.filter_by(username=username).first()
        if(user):
            if(update_form.username.data):
                user.username = update_form.username.data
            if(update_form.email.data):
                user.email = update_form.email.data
            if(update_form.password.data):
                hashed_password = bcrypt.generate_password_hash(
                    update_form.password.data).decode('utf-8')
                user.password = hashed_password
            db.session.commit()
            flash('username '+username+" successfully updated", 'success')
        else:
            flash('unsuccessful operation', 'danger')

        return redirect(url_for(default_url))
    messages = []
    for field, errors in update_form.errors.items():
        messages.append((', '.join(errors)))
    for message in messages:
        flash(message, 'danger')
    return redirect(url_for(default_url))
