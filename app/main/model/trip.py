from .. import db
from ..model.users_trips import users_trips


class Trip(db.Model):
    __tablename__ = "trip"

    name_min_length = 2
    name_max_length = 20

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), unique=False)
    picture_path = db.Column(db.String(255), unique=False)
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    closed = db.Column(db.Boolean, default=False)

    users_trips = db.relationship('User', secondary=users_trips)

    def close(self):
        self.closed = True
