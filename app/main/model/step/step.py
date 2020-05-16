from app.main import db
from app.main.model.users_steps import users_steps


class Step(db.Model):
    __tablename__ = "step"

    name_min_length = 2
    name_max_length = 20

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    trip_id = db.Column(db.Integer, db.ForeignKey('trip.id'))
    name = db.Column(db.String(name_max_length), unique=False)
    start_datetime = db.Column(db.DateTime)
    end_datetime = db.Column(db.DateTime)
    address = db.Column(db.String(100))
    phone_number = db.Column(db.String(15))
    type = db.Column(db.String(15))

    users_steps = db.relationship('User', secondary=users_steps)

    __mapper_args__ = {
        'polymorphic_identity': 'step',
        'polymorphic_on': type
    }
