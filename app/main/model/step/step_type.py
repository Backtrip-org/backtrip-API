from enum import Enum


class StepType(Enum):
    Base = 0
    Food = 1
    Leisure = 2
    Lodging = 3
    Transport = 4
    TransportBus = 5
    TransportTaxi = 6
    TransportPlane = 7
    TransportTrain = 8

    @staticmethod
    def from_string(string_file_type):
        if not StepType.__dict__.__contains__(string_file_type):
            return StepType.Base;
        return StepType.__dict__[string_file_type];


def get_transport_step_types():
    return [StepType.Transport,
            StepType.TransportBus,
            StepType.TransportTrain,
            StepType.TransportTaxi,
            StepType.TransportPlane]
