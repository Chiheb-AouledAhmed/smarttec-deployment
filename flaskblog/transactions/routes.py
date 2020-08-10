import hashlib
from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog import db, bcrypt
from flaskblog.models import User, Post
from flaskblog.users.forms import *
from flaskblog.users.utils import save_picture, send_reset_email

trans = Blueprint('trans', __name__)


@trans.route("/payment", methods=['GET', 'POST'])
def payment():
    NumSite = "5"  # Commmuniqué par GPG checkout
    Password = "5"  # Commmuniqué par GPG checkout
    orderID = "5"
    Currency = "5"
    signature = hashlib.sha1((NumSite+Password+orderID+Currency).encode())
    return render_template('payment.html', NumSite=NumSite,
                           Password=Password, orderID=orderID, Currency=Currency, signature=signature)


@trans.route("/paiement_process.php", methods=['GET', 'POST'])
def payment_check():
    if(request.method == 'POST'):
        print(request.json)
    return redirect(url_for('main.home'))
