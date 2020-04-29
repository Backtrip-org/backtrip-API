from .. import db


class Step(db.Model):
    __tablename__ = "step"

    name_min_length = 2
    name_max_length = 20

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    trip_id = db.Column(db.Integer, db.ForeignKey('trip.id'))
    name = db.Column(db.String(name_max_length), unique=False)
    start_datetime = db.Column(db.DateTime)
