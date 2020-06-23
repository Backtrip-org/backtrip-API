import datetime
import unittest

from app.main import db
from app.main.model.file.file import File
from app.main.model.step.step import Step

from app.main.model.trip import Trip
from app.main.model.user import User
from app.main.service.travel_journal_service import TravelJournalService
from app.main.service.trip_service import create_trip, create_step, add_file_to_step
from app.main.service.user_service import create_user
from app.main.util.exception.TripException import TripMustBeClosedException
from app.test.base import BaseTestCase


def create_test_user() -> User:
    user = User(
        firstname='Jean',
        lastname='Dupont',
        email='test@test.fr',
        password='password',
        registered_on=datetime.datetime.utcnow()
    )
    create_user(user)
    return User.query.filter_by(email=user.email).first()


def create_test_trip(creator: User, closed: bool) -> Trip:
    trip = Trip(
        name='Road-trip Tanzanie',
        picture_path="picture/path",
        creator_id=creator.id,
        closed=closed,
        users_trips=[creator]
    )
    return create_trip(trip)


def add_test_step(trip: Trip, participants: [User], name: str, start_datetime: datetime, end_datetime=None) -> Step:
    step = Step(
        name=name,
        trip_id=trip.id,
        start_datetime=start_datetime,
        end_datetime=end_datetime,
        users_steps=participants
    )

    return create_step(step)


def add_photo_to_test_step(step_id: int, name: str, extension: str):
    photo = File(
        id=name,
        name=name,
        extension=extension,
        type='Photo'
    )

    db.session.add(photo)
    db.session.commit()

    add_file_to_step(photo.id, step_id)


class MyTestCase(BaseTestCase):
    def test_travel_journal_creation(self):
        user = create_test_user()
        trip = create_test_trip(user, closed=True)

        step_1 = add_test_step(trip, [user], 'Safari', datetime.datetime(2020, 5, 21, 15, 00), datetime.datetime(2020, 5, 21, 16, 00))
        add_photo_to_test_step(step_1.id, 'test/test_picture_safari', "jpg")
        step_2 = add_test_step(trip, [user], 'Repas', datetime.datetime(2020, 5, 21, 19, 00))
        add_photo_to_test_step(step_2.id, 'test/test_picture_restaurant', 'jpg')
        step_3 = add_test_step(trip, [user], 'Hotel', datetime.datetime(2020, 5, 21, 21, 00))
        add_photo_to_test_step(step_3.id, 'test/test_picture_hotel', 'jpg')
        step_4 = add_test_step(trip, [user], 'Concert', datetime.datetime(2020, 5, 21, 22, 00))
        add_photo_to_test_step(step_4.id, 'test/test_picture_concert', 'jpg')

        TravelJournalService(trip, user).generate_travel_journal()

    def test_travel_creation_with_open_trip_should_raise_exception(self):
        user = create_test_user()
        trip = create_test_trip(user, closed=False)
        with self.assertRaises(TripMustBeClosedException):
            TravelJournalService(trip, user)




if __name__ == '__main__':
    unittest.main()
