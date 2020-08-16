
import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from flaskblog import mail
from werkzeug.utils import secure_filename


def save_document(form_document):
    filename = secure_filename(form_document.filename)
    document_fn = filename
    document_path = os.path.join(
        current_app.root_path, 'static/uploaded_documents', document_fn)

    form_document.save(document_path)

    return document_fn
