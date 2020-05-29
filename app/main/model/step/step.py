from app.main import db
from app.main.model.step.step_type import StepType
from app.main.model.steps_files import steps_files
from app.main.model.users_steps import users_steps


class Step(db.Model):
    __tablename__ = "step"

    name_min_length = 2
    name_max_length = 20

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    trip_id = db.Column(db.Integer, db.ForeignKey('trip.id'))
    name = db.Column(db.String(name_max_length), nullable=False, unique=False)
    start_datetime = db.Column(db.DateTime, nullable=False)
    end_datetime = db.Column(db.DateTime)
    start_address = db.Column(db.String(100))
    phone_number = db.Column(db.String(15))
    notes = db.Column(db.String(200))
    type = db.Column(db.String(15))

    users_steps = db.relationship('User', secondary=users_steps)
    files = db.relationship('File', secondary=steps_files)

    __mapper_args__ = {
        'polymorphic_identity': StepType.Base.name,
        'polymorphic_on': type
    }
