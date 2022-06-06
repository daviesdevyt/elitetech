from . import socketio, db
from flask_socketio import emit
from flask_login import login_required, current_user
from flask import session, request
from datetime import timedelta, datetime

@socketio.on('connect', namespace='/game')
@login_required
def connected():
    if not current_user.mining:
        start_mine()
    current_user.sid = request.sid
    db.session.commit()
    session[request.sid] = 0
    emit('getBalance', current_user.get_balance())

@socketio.on('disconnect', namespace='/game')
@login_required
def disconnected():
    emit('getBalance', current_user.get_balance())

@socketio.on('gameOver', namespace='/game')
@login_required
def game_over():
    if current_user.earned_today > 20:
        emit('earningLimit')
        return
    current_user.earned_today += session[current_user.sid]
    current_user.earned += session[current_user.sid]
    session[current_user.sid] = 0
    db.session.commit()
    emit('getBalance', current_user.get_balance())

@socketio.on('addToken', namespace='/game')
@login_required
def add_tokens():
    session[current_user.sid] += 0.05
    emit('getBalance', current_user.get_balance())

@socketio.on('connect', namespace='/account')
@login_required
def connect():
    if (current_user.started_mining + timedelta(days=1)-datetime.now()).days < 0 and current_user.mining:
        current_user.mining = False
        db.session.commit()
    data = {"mining": current_user.mining, 'next': str(current_user.started_mining + timedelta(days=1)), "current_time": str(datetime.now())}
    emit('miningStatus', data)


@socketio.on('startMine', namespace='/account')
@login_required
def start_mine():
    if current_user.mining == True:
        return
    current_user.earned_today = 0
    current_user.mining = True
    current_user.mined += 10
    current_user.started_mining = datetime.now()
    db.session.commit()
    print(current_user.mining, current_user.started_mining)
    connect()
    emit('getBalance', current_user.get_balance())
