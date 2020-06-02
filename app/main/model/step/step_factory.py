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

    def get(self, step_dto, trip_id):
        step_type = step_dto.get('type')

        step_objects = {
            StepType.Base.name: lambda dto: Step.from_json(dto, trip_id),
            StepType.Food.name: lambda dto: StepFood.from_json(dto, trip_id),
            StepType.Leisure.name: lambda dto: StepLeisure.from_json(dto, trip_id),
            StepType.Lodging.name: lambda dto: StepLodging.from_json(dto, trip_id),
            StepType.Transport.name: lambda dto: StepTransport.from_json(dto, trip_id),
            StepType.TransportBus.name: lambda dto: StepTransportBus.from_json(dto, trip_id),
            StepType.TransportPlane.name: lambda dto: StepTransportPlane.from_json(dto, trip_id),
            StepType.TransportTaxi.name: lambda dto: StepTransportTaxi.from_json(dto, trip_id),
            StepType.TransportTrain.name: lambda dto: StepTransportTrain.from_json(dto, trip_id),
        }

        if step_type not in step_objects:
            raise UnknownStepTypeException(step_type)

        return step_objects.get(step_type)(step_dto)


