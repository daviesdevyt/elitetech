from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(128), unique=True)
    password = db.Column(db.String(128))
    earned = db.Column(db.Float, default=0)
    mined = db.Column(db.Float, default=0)
    started_mining = db.Column(db.DateTime, default=func.now())
    mining = db.Column(db.Boolean, default=False)
    sid = db.Column(db.Text)
    subscribed = db.Column(db.Boolean, default=False)
    def get_balance(self):
        return self.mined+self.earned

class Subscription(db.Model):
    email = db.Column(db.Text, primary_key=True)


def circulating_supply():
    t = 0
    for i in User.query.all():
        t += i.mined+i.earned
    t = round(t, 5)
    return t