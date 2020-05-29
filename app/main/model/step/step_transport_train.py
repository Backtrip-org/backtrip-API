from app.main import db
from app.main.model.step.step_transport import StepTransport
from app.main.model.step.step_type import StepType


class StepTransportTrain(StepTransport):
    __tablename__ = 'step_transport_train'
    id = db.Column(db.Integer, db.ForeignKey('step_transport.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': StepType.TransportTrain.name,
    }
