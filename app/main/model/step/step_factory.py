from app.main.model.place.place import Place
from app.main.model.step.step import Step
from app.main.model.step.step_food import StepFood
from app.main.model.step.step_leisure import StepLeisure
from app.main.model.step.step_lodging import StepLodging
from app.main.model.step.step_transport import StepTransport
from app.main.model.step.step_transport_bus import StepTransportBus
from app.main.model.step.step_transport_plane import StepTransportPlane
from app.main.model.step.step_transport_taxi import StepTransportTaxi
from app.main.model.step.step_transport_train import StepTransportTrain
from app.main.model.step.step_type import StepType
from app.main.util.exception.StepException import UnknownStepTypeException


class StepFactory:

    def __init__(self, step_dto, trip_id):
        self.step_dto = step_dto
        self.trip_id = trip_id

    def get(self):
        step_type = self.step_dto.get('type')

        step_objects = {
            StepType.Base.name: self.basic_step(),
            StepType.Food.name: self.food_step(),
            StepType.Leisure.name: self.leisure_step(),
            StepType.Lodging.name: self.lodging_step(),
            StepType.Transport.name: self.transport_step(),
            StepType.TransportBus.name: self.transport_bus_step(),
            StepType.TransportPlane.name: self.transport_plane_step(),
            StepType.TransportTaxi.name: self.transport_taxi_step(),
            StepType.TransportTrain.name: self.transport_train_step()
        }

        if step_type not in step_objects:
            raise UnknownStepTypeException(step_type)

        return step_objects.get(step_type)

    def basic_step(self):
        return Step(
            name=self.step_dto.get('name'),
            trip_id=self.trip_id,
            start_datetime=self.step_dto.get('start_datetime'),
            end_datetime=self.step_dto.get('end_datetime'),
            start_address=Place.from_json(self.step_dto.get('start_address')),
            phone_number=self.step_dto.get('phone_number'),
            notes=self.step_dto.get('notes')
        )

    def food_step(self):
        return StepFood(
            name=self.step_dto.get('name'),
            trip_id=self.trip_id,
            start_datetime=self.step_dto.get('start_datetime'),
            end_datetime=self.step_dto.get('end_datetime'),
            start_address=Place.from_json(self.step_dto.get('start_address')),
            phone_number=self.step_dto.get('phone_number'),
            notes=self.step_dto.get('notes')
        )

    def leisure_step(self):
        return StepLeisure(
            name=self.step_dto.get('name'),
            trip_id=self.trip_id,
            start_datetime=self.step_dto.get('start_datetime'),
            end_datetime=self.step_dto.get('end_datetime'),
            start_address=Place.from_json(self.step_dto.get('start_address')),
            phone_number=self.step_dto.get('phone_number'),
            notes=self.step_dto.get('notes')
        )

    def lodging_step(self):
        return StepLodging(
            name=self.step_dto.get('name'),
            trip_id=self.trip_id,
            start_datetime=self.step_dto.get('start_datetime'),
            end_datetime=self.step_dto.get('end_datetime'),
            start_address=Place.from_json(self.step_dto.get('start_address')),
            phone_number=self.step_dto.get('phone_number'),
            notes=self.step_dto.get('notes')
        )

    def transport_step(self):
        return StepTransport(
            name=self.step_dto.get('name'),
            trip_id=self.trip_id,
            start_datetime=self.step_dto.get('start_datetime'),
            end_datetime=self.step_dto.get('end_datetime'),
            start_address=Place.from_json(self.step_dto.get('start_address')),
            end_address=Place.from_json(self.step_dto.get('end_address')),
            phone_number=self.step_dto.get('phone_number'),
            notes=self.step_dto.get('notes'),
            reservation_number=self.step_dto.get('reservation_number'),
            transport_number=self.step_dto.get('transport_number')
        )

    def transport_bus_step(self):
        return StepTransportBus(
            name=self.step_dto.get('name'),
            trip_id=self.trip_id,
            start_datetime=self.step_dto.get('start_datetime'),
            end_datetime=self.step_dto.get('end_datetime'),
            start_address=Place.from_json(self.step_dto.get('start_address')),
            end_address=Place.from_json(self.step_dto.get('end_address')),
            phone_number=self.step_dto.get('phone_number'),
            notes=self.step_dto.get('notes'),
            reservation_number=self.step_dto.get('reservation_number'),
            transport_number=self.step_dto.get('transport_number')
        )

    def transport_plane_step(self):
        return StepTransportPlane(
            name=self.step_dto.get('name'),
            trip_id=self.trip_id,
            start_datetime=self.step_dto.get('start_datetime'),
            end_datetime=self.step_dto.get('end_datetime'),
            start_address=Place.from_json(self.step_dto.get('start_address')),
            end_address=Place.from_json(self.step_dto.get('end_address')),
            phone_number=self.step_dto.get('phone_number'),
            notes=self.step_dto.get('notes'),
            reservation_number=self.step_dto.get('reservation_number'),
            transport_number=self.step_dto.get('transport_number')
        )

    def transport_taxi_step(self):
        return StepTransportTaxi(
            name=self.step_dto.get('name'),
            trip_id=self.trip_id,
            start_datetime=self.step_dto.get('start_datetime'),
            end_datetime=self.step_dto.get('end_datetime'),
            start_address=Place.from_json(self.step_dto.get('start_address')),
            end_address=Place.from_json(self.step_dto.get('end_address')),
            phone_number=self.step_dto.get('phone_number'),
            notes=self.step_dto.get('notes'),
            reservation_number=self.step_dto.get('reservation_number'),
            transport_number=self.step_dto.get('transport_number')
        )

    def transport_train_step(self):
        return StepTransportTrain(
            name=self.step_dto.get('name'),
            trip_id=self.trip_id,
            start_datetime=self.step_dto.get('start_datetime'),
            end_datetime=self.step_dto.get('end_datetime'),
            start_address=Place.from_json(self.step_dto.get('start_address')),
            end_address=Place.from_json(self.step_dto.get('end_address')),
            phone_number=self.step_dto.get('phone_number'),
            notes=self.step_dto.get('notes'),
            reservation_number=self.step_dto.get('reservation_number'),
            transport_number=self.step_dto.get('transport_number')
        )



