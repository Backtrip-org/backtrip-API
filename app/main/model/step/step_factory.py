from app.main.model.step.step import Step
from app.main.model.step.step_food import StepFood
from app.main.model.step.step_leisure import StepLeisure
from app.main.model.step.step_lodging import StepLodging
from app.main.model.step.step_transport import StepTransport
from app.main.model.step.step_type import StepType
from app.main.util.exception.StepException import UnknownStepTypeException


class StepFactory:

    def __init__(self, step_dto, trip_id):
        self.step_dto = step_dto
        self.trip_id = trip_id

    def get(self):
        step_type = self.step_dto.get('type')

        if step_type == StepType.Base.name:
            return self.basic_step()
        elif step_type == StepType.Food.name:
            return self.food_step()
        elif step_type == StepType.Leisure.name:
            return self.leisure_step()
        elif step_type == StepType.Lodging.name:
            return self.lodging_step()
        elif step_type == StepType.Transport.name:
            return self.transport_step()

        raise UnknownStepTypeException(step_type)

    def basic_step(self):
        return Step(
            name=self.step_dto.get('name'),
            trip_id=self.trip_id,
            start_datetime=self.step_dto.get('start_datetime'),
            end_datetime=self.step_dto.get('end_datetime'),
            start_address=self.step_dto.get('start_address'),
            phone_number=self.step_dto.get('phone_number'),
            notes=self.step_dto.get('notes')
        )

    def food_step(self):
        return StepFood(
            name=self.step_dto.get('name'),
            trip_id=self.trip_id,
            start_datetime=self.step_dto.get('start_datetime'),
            end_datetime=self.step_dto.get('end_datetime'),
            start_address=self.step_dto.get('start_address'),
            phone_number=self.step_dto.get('phone_number'),
            notes=self.step_dto.get('notes')
        )

    def leisure_step(self):
        return StepLeisure(
            name=self.step_dto.get('name'),
            trip_id=self.trip_id,
            start_datetime=self.step_dto.get('start_datetime'),
            end_datetime=self.step_dto.get('end_datetime'),
            start_address=self.step_dto.get('start_address'),
            phone_number=self.step_dto.get('phone_number'),
            notes=self.step_dto.get('notes')
        )

    def lodging_step(self):
        return StepLodging(
            name=self.step_dto.get('name'),
            trip_id=self.trip_id,
            start_datetime=self.step_dto.get('start_datetime'),
            end_datetime=self.step_dto.get('end_datetime'),
            start_address=self.step_dto.get('start_address'),
            phone_number=self.step_dto.get('phone_number'),
            notes=self.step_dto.get('notes')
        )

    def transport_step(self):
        return StepTransport(
            name=self.step_dto.get('name'),
            trip_id=self.trip_id,
            start_datetime=self.step_dto.get('start_datetime'),
            end_datetime=self.step_dto.get('end_datetime'),
            start_address=self.step_dto.get('start_address'),
            end_address=self.step_dto.get('end_address'),
            phone_number=self.step_dto.get('phone_number'),
            notes=self.step_dto.get('notes'),
            reservation_number=self.step_dto.get('reservation_number'),
            transport_number=self.step_dto.get('transport_number')
        )


