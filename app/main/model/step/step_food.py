from app.main import db
from app.main.model.place.place import Place
from app.main.model.step.step import Step
from app.main.model.step.step_type import StepType


class StepFood(Step):
    __tablename__ = 'step_food'
    id = db.Column(db.Integer, db.ForeignKey('step.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': StepType.Food.name,
    }

    @staticmethod
    def from_json(dto, trip_id):
        return StepFood(
            name=dto.get('name'),
            trip_id=trip_id,
            start_datetime=dto.get('start_datetime'),
            end_datetime=dto.get('end_datetime'),
            start_address=Place.from_json(dto.get('start_address')),
            phone_number=dto.get('phone_number'),
            notes=dto.get('notes')
        )