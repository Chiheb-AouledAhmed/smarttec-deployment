from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.models import *
from flaskblog.posts.forms import *
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


@posts.route("/post/<int:post_id>", methods=['GET', 'POST'])
def post(post_id):
    form = PostForm()
    delete_form = DeleteImageForm()
    post = Post.query.get_or_404(post_id)
    subs = Subscription.query.filter_by(
        post_id=post_id).all()
    users = [(User.query.get(sub.user_id), sub.date_posted,
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
    return render_template('formation.html', title=post.title, post=post, form=form, delete_form=delete_form, users=users)


@ posts.route("/subscribe/<int:post_id>")
def subscribe(post_id):
    post = Post.query.get(post_id)
    return render_template('formation_inscri.html', post=post)


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


@ posts.route("/formation_preview/<int:post_id>")
def preview(post_id):
    post = Post.query.get(post_id)
    form = PaymentMethodForm()
    sceances = post.sceances
    return render_template('formation_preview.html', post=post, sceances=sceances, form=form)


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
