from app.main import db
from app.main.model.step.step import Step
from app.main.model.step.step_type import StepType


class StepTransport(Step):
    __tablename__ = 'step_transport'
    id = db.Column(db.Integer, db.ForeignKey('step.id'), primary_key=True)
    end_address_id = db.Column(db.Integer, db.ForeignKey('place.id'))
    reservation_number = db.Column(db.String(30))
    transport_number = db.Column(db.String(30))

    end_address = db.relationship("Place")

    __mapper_args__ = {
        'polymorphic_identity': StepType.Transport.name,
    }
