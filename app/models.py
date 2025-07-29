from . import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(10))  # 'donor' or 'recipient'
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
class Donation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    donor_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    item = db.Column(db.String(150), nullable=False)
    quantity = db.Column(db.String(50))
    description = db.Column(db.Text)
    location = db.Column(db.String(100))
    matched = db.Column(db.Boolean, default=False)

class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    item_needed = db.Column(db.String(150), nullable=False)
    quantity = db.Column(db.String(50))
    reason = db.Column(db.Text)
    location = db.Column(db.String(100))
    fulfilled = db.Column(db.Boolean, default=False)
