from datetime import datetime

from flask_login import UserMixin
from wtforms.validators import ValidationError

from app import db


class RankHistory(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))
    activity_id = db.Column(db.Integer, db.ForeignKey('activity.id', ondelete='CASCADE'))
    date = db.Column(db.DateTime, default=datetime.today().strftime('%m.%d'))
    value = db.Column(db.Integer, default=-5)


class Activity(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    owner = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))
    name = db.Column(db.String(50), default='')
    reward = db.Column(db.Integer, nullable=False)
    is_completed = db.Column(db.Boolean, default=False)

