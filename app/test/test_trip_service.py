import unittest
import datetime

from app.main.model.user import User
from app.main.model.trip import Trip
from app.main.model.step import Step
from app.main.service.trip_service import create_trip, create_step, invite_to_trip, get_step
from app.main.util.exception.TripException import TripAlreadyExistsException, TripNotFoundException
from app.main.util.exception.GlobalException import StringTooLongException
from app.main.util.exception.UserException import UserEmailNotFoundException
from app.test.base import BaseTestCase
from app.main import db


def create_user(email):
    user = User(
        email=email,
        password='password',
        registered_on=datetime.datetime.utcnow()
    )
    db.session.add(user)
    db.session.commit()
    return User.query.filter_by(email=email).first()


def get_trip_object(name, creator_id):
    return Trip(
        name=name,
        picture_path="picture/path",
        creator_id=creator_id
    )


def get_step_object(name, trip_id, start_datetime):
    return Step(
        name=name,
        trip_id=trip_id,
        start_datetime=start_datetime
    )


class TestTripService(BaseTestCase):

    def test_create_trip_should_succeed(self):
        user = create_user("user1@mail.fr")
        trip = create_trip(get_trip_object(name="trip", creator_id=user.id))
        self.assertIsInstance(trip, Trip)

    def test_create_trip_should_raise_tripalreadyexistsexception(self):
        user = create_user("user1@mail.fr")
        trip = get_trip_object(name="trip", creator_id=user.id)
        create_trip(trip)
        with self.assertRaises(TripAlreadyExistsException):
            create_trip(trip)

    def test_create_trip_with_same_name_but_different_creator_should_succeed(self):
        user1 = create_user("user1@mail.fr")
        user2 = create_user("user2@mail.fr")
        create_trip(get_trip_object(name="trip", creator_id=user1.id))
        user2_trip = create_trip(get_trip_object(name="trip", creator_id=user2.id))
        self.assertIsInstance(user2_trip, Trip)

    def test_create_step_should_succeed(self):
        user = create_user("user1@mail.fr")
        trip = create_trip(get_trip_object(name="trip", creator_id=user.id))
        start_datetime = "2020-04-10 21:00:00"
        step = create_step(get_step_object(name="step", trip_id=trip.id, start_datetime=start_datetime))
        self.assertIsInstance(step, Step)

    def test_create_step_should_raise_tripnotfoundexception(self):
        user = create_user("user1@mail.fr")
        trip = create_trip(get_trip_object(name="trip", creator_id=user.id))
        start_datetime = "2020-04-10 21:00:00"

        with self.assertRaises(TripNotFoundException):
            create_step(get_step_object(name="step", trip_id=trip.id + 1, start_datetime=start_datetime))

    def test_create_step_with_long_name_should_raise_strintoolongexeption(self):
        user = create_user("user1@mail.fr")
        trip = create_trip(get_trip_object(name="trip", creator_id=user.id))
        start_datetime = "2020-04-10 21:00:00"
        name = 's' * 30

        with self.assertRaises(StringTooLongException):
            create_step(get_step_object(name=name, trip_id=trip.id, start_datetime=start_datetime))

    def test_invite_to_trip_should_succeed(self):
        creator = create_user("creator@mail.fr")
        participant = create_user("participant@mail.fr")
        trip = create_trip(get_trip_object(name="trip", creator_id=creator.id))
        invite_to_trip(trip_id=trip.id, user_to_invite_email=participant.email)
        participants_email = map(lambda user: user.email, trip.users_trips)
        self.assertTrue(participant.email in participants_email)

    def test_invite_to_trip_should_raise_tripnotfoundexception(self):
        creator = create_user("creator@mail.fr")
        participant = create_user("participant@mail.fr")
        trip = create_trip(get_trip_object(name="trip", creator_id=creator.id))

        with self.assertRaises(TripNotFoundException):
            invite_to_trip(trip_id=trip.id + 1, user_to_invite_email=participant.email)

    def test_invite_to_trip_should_raise_useremailnotfoundexception(self):
        creator = create_user("creator@mail.fr")
        trip = create_trip(get_trip_object(name="trip", creator_id=creator.id))

        with self.assertRaises(UserEmailNotFoundException):
            invite_to_trip(trip_id=trip.id, user_to_invite_email="participant@mail.fr")

    def test_get_step_should_return_step(self):
        user = create_user("user1@mail.fr")
        trip = create_trip(get_trip_object(name="trip", creator_id=user.id))
        start_datetime = "2020-04-10 21:00:00"
        created_step = create_step(get_step_object(name="step", trip_id=trip.id, start_datetime=start_datetime))
        step = get_step(created_step.id)
        self.assertIsInstance(step, Step)

    def test_get_uncreated_step_should_return_none(self):
        user = create_user("user1@mail.fr")
        trip = create_trip(get_trip_object(name="trip", creator_id=user.id))
        start_datetime = "2020-04-10 21:00:00"
        created_step = create_step(get_step_object(name="step", trip_id=trip.id, start_datetime=start_datetime))
        step = get_step(created_step.id + 1)
        self.assertEqual(step, None)


if __name__ == '__main__':
    unittest.main()
