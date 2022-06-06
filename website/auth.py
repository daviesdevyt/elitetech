from flask import Blueprint, render_template, request, flash, json, redirect, url_for, json
from flask_login import login_user, logout_user
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
import hashlib

auth = Blueprint('auth', __name__)

def h(txt):
    encode = json.dumps(txt, sort_keys=True).encode()
    hash_f = hashlib.md5(encode).hexdigest()
    return hash_f[:5]


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('views.home'))

@auth.route('/login', methods=['POST', "GET"])
def login():
    if request.method == 'POST':
        addr = request.form['addr']
        pwd = request.form['pwd']
        user = User.query.filter_by(address=addr).first()
        if not user:
            ref = request.form['ref']
            referrer = User.query.filter_by(referral_code=ref).first()
            if referrer:
                referrer.earned += 100
            user = User(address=addr, password=generate_password_hash(pwd, "sha512"), referral_code=h(addr))
            db.session.add(user)
            db.session.commit()
        else:
            if not check_password_hash(user.password, pwd):
                flash("Incorrect password", "danger")
                return redirect(url_for('auth.login'))
        login_user(user)
        return redirect(url_for('views.account'))
    return render_template("login.html")
