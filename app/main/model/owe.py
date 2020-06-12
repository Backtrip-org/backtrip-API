from .. import db


class Owe(db.Model):
    __tablename__ = "owe"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cost = db.Column(db.DECIMAL(10, 2), unique=False)
    expense_id = db.Column(db.Integer, db.ForeignKey('expense.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
