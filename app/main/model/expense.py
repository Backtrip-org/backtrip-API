from .. import db


class Expense(db.Model):
    __tablename__ = "expense"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cost = db.Column(db.Integer, unique=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    trip_id = db.Column(db.Integer, db.ForeignKey('trip.id'))
