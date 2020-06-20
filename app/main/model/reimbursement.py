from .. import db


class Reimbursement(db.Model):
    __tablename__ = "reimbursement"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cost = db.Column(db.DECIMAL(10, 2), unique=False)
    expense_id = db.Column(db.Integer, db.ForeignKey('expense.id'))
    emitter_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    payee_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    trip_id = db.Column(db.Integer, db.ForeignKey('trip.id'))
