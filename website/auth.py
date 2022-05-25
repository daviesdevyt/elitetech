from datetime import datetime, timedelta
from flask import Blueprint, render_template, request, flash, jsonify, json, session, redirect, url_for
from flask_login import login_required, current_user, login_user, logout_user
from flask_socketio import emit
from . import db
from .models import User

auth = Blueprint('auth', __name__)

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
            user = User(address=addr, password=pwd)
            db.session.add(user)
            db.session.commit()
            print("created")
        else:
            if user.password != pwd:
                return redirect(url_for('auth.login'))
        login_user(user)
        return redirect(url_for('views.account'))
    return render_template("login.html")
