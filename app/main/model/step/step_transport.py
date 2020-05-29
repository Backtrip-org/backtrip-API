from app.main import db
from app.main.model.step.step import Step
from app.main.model.step.step_type import StepType


class StepTransport(Step):
    __tablename__ = 'step_transport'
    id = db.Column(db.Integer, db.ForeignKey('step.id'), primary_key=True)
    reservation_number = db.Column(db.String(30))
    transport_number = db.Column(db.String(30))
    end_address = db.Column(db.String(100))

    __mapper_args__ = {
        'polymorphic_identity': StepType.Transport.name,
    }
