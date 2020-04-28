from .. import db
from ..model.users_trips import users_trips


class Trip(db.Model):
    __tablename__ = "trip"

    name_length = 20

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(name_length), unique=False)
    picture_path = db.Column(db.String(255), unique=False)
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    users_trips = db.relationship('User', secondary=users_trips)
