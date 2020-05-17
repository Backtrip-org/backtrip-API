import unittest

from app.main.model.step.step import Step
from app.main.model.step.step_factory import StepFactory
from app.main.model.step.step_food import StepFood
from app.main.model.step.step_lodging import StepLodging
from app.main.model.step.step_transport import StepTransport
from app.main.model.step.step_transport_bus import StepTransportBus
from app.main.model.step.step_transport_plane import StepTransportPlane
from app.main.model.step.step_transport_taxi import StepTransportTaxi
from app.main.model.step.step_transport_train import StepTransportTrain
from app.main.util.exception.StepException import UnknownStepTypeException
from app.test.base import BaseTestCase


class MyTestCase(BaseTestCase):
    def test_get_unknown_step_should_raise_exception(self):
        step_dto = dict(name='step', start_datetime='2020-04-10 21:00:00', type='Unknown')
        step_factory = StepFactory(step_dto, 0)
        with self.assertRaises(UnknownStepTypeException):
            step_factory.get()

    def test_get_step_should_return_base_step(self):
        step_dto = dict(name='step', start_datetime='2020-04-10 21:00:00', type='Base')
        step = StepFactory(step_dto, 0).get()
        self.assertIsInstance(step, Step)

    def test_get_step_should_return_food_step(self):
        step_dto = dict(name='step', start_datetime='2020-04-10 21:00:00', type='Food')
        step = StepFactory(step_dto, 0).get()
        self.assertIsInstance(step, StepFood)

    def test_get_step_should_return_lodging_step(self):
        step_dto = dict(name='step', start_datetime='2020-04-10 21:00:00', type='Lodging')
        step = StepFactory(step_dto, 0).get()
        self.assertIsInstance(step, StepLodging)

    def test_get_step_should_return_transport_step(self):
        step_dto = dict(name='step', start_datetime='2020-04-10 21:00:00', type='Transport')
        step = StepFactory(step_dto, 0).get()
        self.assertIsInstance(step, StepTransport)

    def test_get_step_should_return_bus_transport_step(self):
        step_dto = dict(name='step', start_datetime='2020-04-10 21:00:00', type='TransportBus')
        step = StepFactory(step_dto, 0).get()
        self.assertIsInstance(step, StepTransportBus)

    def test_get_step_should_return_plane_transport_step(self):
        step_dto = dict(name='step', start_datetime='2020-04-10 21:00:00', type='TransportPlane')
        step = StepFactory(step_dto, 0).get()
        self.assertIsInstance(step, StepTransportPlane)

    def test_get_step_should_return_train_transport_step(self):
        step_dto = dict(name='step', start_datetime='2020-04-10 21:00:00', type='TransportTrain')
        step = StepFactory(step_dto, 0).get()
        self.assertIsInstance(step, StepTransportTrain)

    def test_get_step_should_return_taxi_transport_step(self):
        step_dto = dict(name='step', start_datetime='2020-04-10 21:00:00', type='TransportTaxi')
        step = StepFactory(step_dto, 0).get()
        self.assertIsInstance(step, StepTransportTaxi)


if __name__ == '__main__':
    unittest.main()
