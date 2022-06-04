from datetime import datetime, timedelta
from locale import currency
from flask import Blueprint, render_template, request, flash, jsonify, json, session, redirect, url_for
from flask_login import current_user, login_required
from flask_socketio import emit
from . import db, socketio
from .models import Subscription

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@views.route('/home', methods=['GET', 'POST'])
def home():
    return render_template("index.html")

@views.route('/game', methods=['GET', 'POST'])
@login_required
def game():
    game = request.args['name']
    return render_template("games/"+game+".html")

@views.route('/presale', methods=['GET', 'POST'])
def presale():
    return render_template("presale.html")

@views.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    return render_template("account.html")

@views.route('/games', methods=['GET', 'POST'])
def games():
    return render_template("games.html")

@views.route('/token-abi')
def token_abi():
    with open('website/static/tokenABI.json') as file:
        return jsonify(json.load(file))

@views.route('/swap-abi')
def swap_abi():
    with open('website/static/swapABI.json') as file:
        return jsonify(json.load(file))

@views.route('/newsletter', methods=['GET', "POST"])
def newsletter():
    if request.method=="POST":
        email = request.form['email']
        if not Subscription.query.get(email):
            if current_user: current_user.subscribed = True
            new = Subscription(email=email)
            db.session.add(new)
            db.session.commit()
    return redirect(request.referrer)

@views.route('/whitepaper')
def whitepaper():
    return render_template("whitepaper.html")

@views.route('/nfts')
def nfts():
    return render_template("nfts.html")
