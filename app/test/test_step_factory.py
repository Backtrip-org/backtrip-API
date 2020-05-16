import unittest
import json

from app.main.model.step.step import Step
from app.main.model.step.step_factory import StepFactory
from app.main.model.step.step_food import StepFood
from app.main.model.step.step_lodging import StepLodging
from app.main.util.exception.StepException import UnknownStepTypeException
from app.test.base import BaseTestCase


class MyTestCase(BaseTestCase):
    def test_get_unknown_step_should_raise_exception(self):
        step_dto = dict(name='step', start_datetime='2020-04-10 21:00:00', type='Unknown')
        step_factory = StepFactory(step_dto, 0)
        with self.assertRaises(UnknownStepTypeException):
            step_factory.get()

    def test_get_step_should_return_food_step(self):
        step_dto = dict(name='step', start_datetime='2020-04-10 21:00:00', type='Food')
        step = StepFactory(step_dto, 0).get()
        self.assertIsInstance(step, StepFood)

    def test_get_step_should_return_lodging_step(self):
        step_dto = dict(name='step', start_datetime='2020-04-10 21:00:00', type='Lodging')
        step = StepFactory(step_dto, 0).get()
        self.assertIsInstance(step, StepLodging)

    def test_get_step_should_return_base_step(self):
        step_dto = dict(name='step', start_datetime='2020-04-10 21:00:00', type='Base')
        step = StepFactory(step_dto, 0).get()
        self.assertIsInstance(step, Step)


if __name__ == '__main__':
    unittest.main()
