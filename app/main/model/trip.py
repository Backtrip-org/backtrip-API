from sqlalchemy.orm import relationship

from .. import db


class Trip(db.Model):
    __tablename__ = "trip"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), unique=True)
    picture_path = db.Column(db.String(255), unique=False, default=False)
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'))
