import operator
from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog import db, bcrypt
from flaskblog.models import *
from flaskblog.posts.forms import *
from flaskblog.users.forms import *
from flaskblog.posts.utils import *
posts = Blueprint('posts', __name__)


@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if(current_user.acc_rights == 2):
        flash('You don''t have the rights to acces this page ', 'danger')
        return redirect(url_for('main.home'))
    if form.validate_on_submit():
        post = Post(title=form.title.data,
                    content=form.content.data, author=current_user, start_date=form.date.data,
                    zoom_link=form.zoom_link.data, youtube_url=form.youtube_url.data, price=form.price.data,
                    description=form.description.data, num_posts=form.num_posts.data)
        db.session.add(post)
        db.session.commit()
        for i in range(1, form.num_posts.data+1):
            sceance = Sceance(title=form.title.data +
                              "-Sceance "+str(i), session_id=post.id, start_date=form.date.data, num=i, content="")
            db.session.add(sceance)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('new_post.html', title='New Post',
                           form=form, legend='New Post')


@posts.route("/delete_sub", methods=['GET', 'POST'])
def delete_sub():
    subform = SubForm()
    sub_id = subform.sub_id.data
    sub = Subscription.query.get(sub_id)
    post_id = sub.post_id
    if(sub):
        flash('L''abonnement a été désactivé avec succès', 'success')
    else:
        flash('opération échouée', 'warning')
    db.session.delete(sub)
    db.session.commit()
    return redirect(url_for('posts.post', post_id=post_id))


@posts.route("/post/<int:post_id>", methods=['GET', 'POST'])
def post(post_id):
    form = PostForm()
    subform = SubForm()
    delete_form = DeleteImageForm()
    certif_form = CertificateForm()
    post = Post.query.get_or_404(post_id)
    subs = Subscription.query.filter_by(
        post_id=post_id).all()
    users = [(sub.id, User.query.get(sub.user_id), sub.date_posted,
              sub.payment_method) for sub in subs]
    if(request.method == "POST"):
        if form.validate_on_submit():
            if(form.images.data):
                image_file = save_picture(form.images.data)
                print(image_file)
                cur_image = PostImage(url=image_file, ima_post=post.id)
                db.session.add(cur_image)
                db.session.commit()
            post.title = form.title.data
            post.content = form.content.data
            post.description = form.description.data
            post.start_date = form.date.data
            post.zoom_link = form.zoom_link.data
            post.youtube_url = form.youtube_url.data
            post.price = form.price.data
            post.num_posts = form.num_posts.data
            if(len(post.sceances) > post.num_posts):
                for i in range(post.num_posts, len(post.sceances)):
                    db.session.delete((post.sceances)[i])
            elif(len(post.sceances) < post.num_posts):
                for i in range(len(post.sceances)+1, post.num_posts+1):
                    sceance = Sceance(title=form.title.data + "-Sceance "+str(i),
                                      session_id=post.id, start_date=post.start_date, num=i, content="")
                    db.session.add(sceance)
            db.session.commit()
            print(post.sceances)
            flash('Your post has been updated!', 'success')
            return redirect(url_for('posts.post', post_id=post.id))
        else:
            for field, errors in form.errors.items():
                flash(((', '.join(errors))), 'danger')
            return redirect(url_for('posts.post', post_id=post.id))
    return render_template('formation.html', title=post.title, post=post, form=form, delete_form=delete_form, users=users, certif_form=certif_form, subform=subform)


@ posts.route("/subscribe/<int:post_id>")
def subscribe(post_id):
    post = Post.query.get(post_id)
    return render_template('formation_inscri.html', post=post)


@ posts.route("/search", methods=['GET', 'POST'])
def search():
    form = CertificateForm()
    certifs = []
    for sub in Subscription.query.filter(Subscription.Certif_ref != None).all():
        certif = {"ref": "", "nom": "", "prenom": "",
                  "post": "", "date": "", "score": ""}
        certif['ref'] = sub.Certif_ref
        user = Userinfo.query.filter_by(user_id=sub.user_id).first()
        if(user):
            certif['nom'] = user.Nom
            certif['prenom'] = user.Prenom
        certif['post'] = Post.query.get(sub.post_id).title
        certif['date'] = sub.date_certf
        certif['score'] = sub.Test_score
        certifs.append(certif)
    result = None
    if((form.validate_on_submit) and (request.method == 'POST')):
        print(form.ref.data)
        sub = Subscription.query.filter_by(
            Certif_ref=form.ref.data).first()
        print(sub)
        if(sub):
            certif = {"ref": "", "nom": "", "prenom": "",
                      "post": "", "date": "", "score": ""}
            certif['ref'] = sub.Certif_ref
            user = Userinfo.query.filter_by(user_id=sub.user_id).first()
            if(user):
                certif['nom'] = user.Nom
                certif['prenom'] = user.Prenom
            certif['post'] = Post.query.get(sub.post_id).title
            certif['date'] = sub.date_certf
            certif['score'] = sub.Test_score
            result = certif
        else:
            result = "Ce certificat n'existe pas"
    return render_template('search.html', form=form, certifs=certifs, result=result)


@posts.route("/delete_image", methods=['GET', 'POST'])
def delete_image():
    form = DeleteImageForm()
    if(form.validate_on_submit):
        image = PostImage.query.get(form.image_id.data)
        if(image):
            db.session.delete(image)
            db.session.commit()
            post_id = image.ima_post
            flash("image successfully deleted", 'success')
        else:
            flash("image not found", 'danger')
    return redirect(url_for('posts.post', post_id=post_id))


@posts.route('/new_infos/<int:post_id>', methods=['GET', 'POST'])
def newinfo(post_id):
    form = InfoForm()
    if(form.validate_on_submit):
        userinfo = Userinfo(Nom=form.Nom.data, Prenom=form.Prenom.data, Sexe=form.Sexe.data,
                            Num_tel=form.Num_tel.data, Pays=form.Pays.data, Niv_etude=form.Niv_etude.data, user_id=current_user.id)
        db.session.add(userinfo)
        db.session.commit()
        flash('Vos informations sont sauvegardés avec succès', 'success')
    return redirect(url_for('posts.preview', post_id=post_id))


@ posts.route("/formation_preview/<int:post_id>",  methods=['GET', 'POST'], defaults={'active': False})
@ posts.route("/formation_preview/<int:post_id>/<int:active>", methods=['GET', 'POST'])
def preview(post_id, active):
    post = Post.query.get(post_id)
    form = PaymentMethodForm()
    register_form = RegistrationForm()
    login_form = LoginForm()
    info_form = InfoForm()
    pre_sceances = post.sceances
    sceances = []
    if(current_user.is_authenticated) and ((len(current_user.infos))):
        active = 0
    else:
        active = 1
    print(active)
    for i in range(1, post.num_posts+1):
        for sc in pre_sceances:
            if(sc.num == i):
                sceances.append(sc)
                break
    if register_form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            register_form.password.data).decode('utf-8')
        user = User(username=register_form.username.data,
                    email=register_form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(
            'Votre compte a été créée et vous êtes inscris dans cette formation', 'success')
        login_user(user, remember=login_form.remember.data)
        return redirect(url_for('posts.preview', post_id=post_id, active=True))
    if login_form.validate_on_submit():
        user = User.query.filter_by(email=login_form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, login_form.password.data):
            login_user(user, remember=login_form.remember.data)
            next_page = request.args.get('next')
            flash(
                'Vous êtes inscris dans cette formation', 'success')
            return redirect(next_page) if next_page else redirect(url_for('posts.preview', post_id=post_id, active=True))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('formation_preview.html', post=post, sceances=sceances, form=form,
                           register_form=register_form, login_form=login_form, active=active, info_form=info_form)


@ posts.route("/subscription/<int:user_id>/<int:post_id>", methods=['GET', 'POST'])
def subscription(user_id, post_id):
    form = PaymentMethodForm()
    if(request.method == 'POST'):
        payment_method = form.mode_de_paiement.data
        subscription = Subscription(
            user_id=user_id, post_id=post_id, payment_method=payment_method)
        db.session.add(subscription)
        db.session.commit()
        flash('votre inscription a été réussite', 'success')
    return redirect(url_for('main.home'))


@ posts.route("/certif", methods=['GET', 'POST'])
def certif():
    form = CertificateForm()
    if(form.validate_on_submit):
        ref = form.ref.data
        score = form.score.data
        id = form.cert_id.data
        print(id)
        sub = Subscription.query.get(id)
        sub.Certif_ref = ref
        sub.Test_score = score
        sub.date_certf = datetime.utcnow()
        db.session.commit()
        flash('Certificat ajoutée avec succès', 'success')
    return redirect(url_for('posts.post', post_id=sub.post_id))


@ posts.route("/post/<int:post_id>/<int:sceance_id>", methods=['GET', 'POST'])
def sceance(post_id, sceance_id):
    form = SceanceForm()
    delete_form = DeleteImageForm()
    sceance = ""
    for sc in Post.query.get(post_id).sceances:
        if(sc.num == sceance_id):
            sceance = sc
    documents = [doc.url for doc in sceance.documents]
    if form.validate_on_submit():
        if form.document.data:
            doc_file = save_document(form.document.data)
            cur_document = Document(
                start=form.date.data, end=datetime(2070, 1, 1, 23, 59), url=doc_file, sceance=sceance.id)
            db.session.add(cur_document)
            db.session.commit()

        sceance.title = form.title.data
        sceance.content = form.content.data
        sceance.date = form.date.data
        sceance.zoom_video = form.zoom_video.data
        db.session.commit()
        flash('La sceance a été mise à jour!', 'success')
        return redirect(url_for('posts.sceance', post_id=post_id, sceance_id=sceance_id))
    return render_template('sceance.html', form=form, sceance=sceance, documents=documents, delete_form=delete_form, post=post)


@ posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@ login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')


@ posts.route("/post/<int:post_id>/delete", methods=['POST'])
@ login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.home'))
