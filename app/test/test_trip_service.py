import unittest
import datetime

from app.main.model.user import User
from app.main.model.trip import Trip
from app.main.service.trip_service import create_trip
from app.main.util.exception.TripException import TripAlreadyExistsException
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


if __name__ == '__main__':
    unittest.main()
