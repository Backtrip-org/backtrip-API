from .. import db


class Step(db.Model):
    __tablename__ = "step"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    trip_id = db.Column(db.Integer, db.ForeignKey('trip.id'))
    name = db.Column(db.String(20), unique=False)
    start_datetime = db.Column(db.DateTime)
