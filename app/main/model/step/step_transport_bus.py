from app.main import db
from app.main.model.step.step_transport import StepTransport
from app.main.model.step.step_type import StepType


class StepTransportBus(StepTransport):
    __tablename__ = 'step_transport_bus'
    id = db.Column(db.Integer, db.ForeignKey('step_transport.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': StepType.TransportBus.name,
    }
