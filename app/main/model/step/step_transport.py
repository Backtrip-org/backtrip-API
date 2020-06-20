from app.main import db
from app.main.model.place.place import Place
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

    @staticmethod
    def from_json(dto, trip_id):
        return StepTransport(
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
