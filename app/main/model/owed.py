from .. import db


class Owed(db.Model):
    __tablename__ = "owed"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cost = db.Column(db.Integer, unique=False)
    expenditure_id = db.Column(db.Integer, db.ForeignKey('expense.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
