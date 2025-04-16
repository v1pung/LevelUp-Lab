from datetime import datetime
from flask_login import UserMixin
from app import db
from ..extensions import login_manager
from ..ranks.model import RankHistory, Activity


class Users(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(30), unique=True)
    psw = db.Column(db.String(300), nullable=True)
    date = db.Column(db.DateTime, default=datetime.now)
    avatar = db.Column(db.String(200), default='')
    rank = db.Column(db.Integer, default=0)
    history = db.relationship(RankHistory, backref='users', lazy="dynamic")
    activities = db.relationship(Activity, backref='users', lazy="dynamic")

    def __repr__(self):
        return f"<user {self.id}, rank {self.rank}"


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))
