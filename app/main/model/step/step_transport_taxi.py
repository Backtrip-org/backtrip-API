from app.main import db
from app.main.model.place.place import Place
from app.main.model.step.step_transport import StepTransport
from app.main.model.step.step_type import StepType


class StepTransportTaxi(StepTransport):
    __tablename__ = 'step_transport_taxi'
    id = db.Column(db.Integer, db.ForeignKey('step_transport.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': StepType.TransportTaxi.name,
    }

    @staticmethod
    def from_json(dto, trip_id):
        return StepTransportTaxi(
            name=dto.get('name'),
            trip_id=trip_id,
            start_datetime=dto.get('start_datetime'),
            end_datetime=dto.get('end_datetime'),
            start_address=Place.from_json(dto.get('start_address')),
            end_address=Place.from_json(dto.get('end_address')),
            phone_number=dto.get('phone_number'),
            notes=dto.get('notes'),
            reservation_number=dto.get('reservation_number'),
            transport_number=dto.get('transport_number')
        )
