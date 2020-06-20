import unittest
import datetime

from app.main.model.expense import Expense
from app.main.model.operation import Operation
from app.main.model.reimbursement import Reimbursement
from app.main.model.user import User
from app.main.model.trip import Trip
from app.main.model.step.step import Step
from app.main.service.trip_service import create_trip, create_step, invite_to_trip, get_step, get_timeline, \
    get_finished_trips_by_user, get_ongoing_trips_by_user, get_coming_trips_by_user, add_participant_to_step, \
    get_user_steps_participation, calculate_future_operations, get_user_reimbursements, refunds_to_get_for_user, \
    create_reimbursement, create_expense
from app.main.util.exception.StepException import StepNotFoundException
from app.main.util.exception.TripException import TripAlreadyExistsException, TripNotFoundException
from app.main.util.exception.GlobalException import StringLengthOutOfRangeException
from app.main.util.exception.UserException import UserEmailNotFoundException, UserIdNotFoundException, \
    UserDoesNotParticipatesToTrip
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


def get_trip_object(name, creator):
    return Trip(
        name=name,
        picture_path="picture/path",
        creator_id=creator.id,
        closed=False,
        users_trips=[creator]
    )


def get_step_object(name, trip_id, start_datetime):
    return Step(
        name=name,
        trip_id=trip_id,
        start_datetime=start_datetime
    )

def get_expense_object(cost, user_id, trip_id):
    return Expense(
        cost=cost,
        trip_id=trip_id,
        user_id=user_id
    )


def get_reimbursement_object(cost, expense_id, emitter_id, payee_id, trip_id):
    return Reimbursement(
        cost=cost,
        expense_id=expense_id,
        emitter_id=emitter_id,
        payee_id=payee_id,
        trip_id=trip_id
    )

def close_trip(trip):
    trip.closed = True
    return trip


def create_trips(trips):
    created_trips = list(map(create_trip, trips))
    return created_trips


def get_closed_trips(user):
    closed_trips = [get_trip_object("closed1", user), get_trip_object("closed2", user)]

    closed_trips = list(map(close_trip, closed_trips))
    closed_trips = create_trips(closed_trips)
    return closed_trips


def get_ongoing_trips(user, current_date=datetime.date.today()):
    ongoing_trips = [get_trip_object("ongoing1", user)]
    ongoing_trips = create_trips(ongoing_trips)
    for trip in ongoing_trips:
        create_step(get_step_object(name="first",
                                    trip_id=trip.id,
                                    start_datetime=datetime.datetime(
                                        current_date.year,
                                        current_date.month,
                                        current_date.day,
                                        8, 0, 0)
                                    ))
        create_step(get_step_object(name="second",
                                    trip_id=trip.id,
                                    start_datetime=datetime.datetime(
                                        current_date.year,
                                        current_date.month,
                                        current_date.day,
                                        10, 0, 0)
                                    ))
    return ongoing_trips


def get_coming_trips(user, current_date=datetime.date.today()):
    coming_trips = [get_trip_object("coming1", user), get_trip_object("coming2", user)]
    coming_trips = create_trips(coming_trips)
    for trip in coming_trips:
        create_step(get_step_object(name="first",
                                    trip_id=trip.id,
                                    start_datetime=datetime.datetime(
                                        current_date.year,
                                        current_date.month,
                                        current_date.day + 1,
                                        8, 0, 0)
                                    ))
        create_step(get_step_object(name="second",
                                    trip_id=trip.id,
                                    start_datetime=datetime.datetime(
                                        current_date.year,
                                        current_date.month,
                                        current_date.day + 1,
                                        10, 0, 0)
                                    ))

    coming_trips.append(create_trip(get_trip_object("no steps", user)))
    return coming_trips


def get_preset_trips(user, current_date=datetime.date.today()):
    closed_trips = get_closed_trips(user)
    ongoing_trips = get_ongoing_trips(user, current_date)
    coming_trips = get_coming_trips(user, current_date)
    all_trips = [closed_trips, ongoing_trips, coming_trips]
    return all_trips, closed_trips, ongoing_trips, coming_trips


class TestTripService(BaseTestCase):

    def test_create_trip_should_succeed(self):
        user = create_user("user1@mail.fr")
        trip = create_trip(get_trip_object(name="trip", creator=user))
        self.assertIsInstance(trip, Trip)

    def test_create_trip_should_raise_tripalreadyexistsexception(self):
        user = create_user("user1@mail.fr")
        trip = get_trip_object(name="trip", creator=user)
        create_trip(trip)
        with self.assertRaises(TripAlreadyExistsException):
            create_trip(trip)

    def test_create_trip_with_same_name_but_different_creator_should_succeed(self):
        user1 = create_user("user1@mail.fr")
        user2 = create_user("user2@mail.fr")
        create_trip(get_trip_object(name="trip", creator=user1))
        user2_trip = create_trip(get_trip_object(name="trip", creator=user2))
        self.assertIsInstance(user2_trip, Trip)

    def test_create_trip_should_set_closed_to_false(self):
        user = create_user("user1@mail.fr")
        trip = create_trip(get_trip_object(name="trip", creator=user))
        self.assertEqual(trip.closed, False)

    def test_create_trip_with_no_name_should_raise_stringlengthoutofrangeexception(self):
        user = create_user("user1@mail.fr")
        trip = get_trip_object(name='', creator=user)
        with self.assertRaises(StringLengthOutOfRangeException):
            create_trip(trip)

    def test_create_step_should_succeed(self):
        user = create_user("user1@mail.fr")
        trip = create_trip(get_trip_object(name="trip", creator=user))
        start_datetime = "2020-04-10 21:00:00"
        step = create_step(get_step_object(name="step", trip_id=trip.id, start_datetime=start_datetime))
        self.assertIsInstance(step, Step)

    def test_create_step_should_raise_tripnotfoundexception(self):
        user = create_user("user1@mail.fr")
        trip = create_trip(get_trip_object(name="trip", creator=user))
        start_datetime = "2020-04-10 21:00:00"

        with self.assertRaises(TripNotFoundException):
            create_step(get_step_object(name="step", trip_id=trip.id + 1, start_datetime=start_datetime))

    def test_create_step_with_long_name_should_raise_stringlengthoutofrangeexception(self):
        user = create_user("user1@mail.fr")
        trip = create_trip(get_trip_object(name="trip", creator=user))
        start_datetime = "2020-04-10 21:00:00"
        name = 's' * 30

        with self.assertRaises(StringLengthOutOfRangeException):
            create_step(get_step_object(name=name, trip_id=trip.id, start_datetime=start_datetime))

    def test_create_step_with_no_name_should_raise_stringlengthoutofrangeexception(self):
        user = create_user("user1@mail.fr")
        trip = create_trip(get_trip_object(name="trip", creator=user))
        start_datetime = "2020-04-10 21:00:00"
        name = ''

        with self.assertRaises(StringLengthOutOfRangeException):
            create_step(get_step_object(name=name, trip_id=trip.id, start_datetime=start_datetime))

    def test_invite_to_trip_should_succeed(self):
        creator = create_user("creator@mail.fr")
        participant = create_user("participant@mail.fr")
        trip = create_trip(get_trip_object(name="trip", creator=creator))
        invite_to_trip(trip_id=trip.id, user_to_invite_email=participant.email)
        participants_email = map(lambda user: user.email, trip.users_trips)
        self.assertTrue(participant.email in participants_email)

    def test_invite_to_trip_should_raise_tripnotfoundexception(self):
        creator = create_user("creator@mail.fr")
        participant = create_user("participant@mail.fr")
        trip = create_trip(get_trip_object(name="trip", creator=creator))

        with self.assertRaises(TripNotFoundException):
            invite_to_trip(trip_id=trip.id + 1, user_to_invite_email=participant.email)

    def test_invite_to_trip_should_raise_useremailnotfoundexception(self):
        creator = create_user("creator@mail.fr")
        trip = create_trip(get_trip_object(name="trip", creator=creator))

        with self.assertRaises(UserEmailNotFoundException):
            invite_to_trip(trip_id=trip.id, user_to_invite_email="participant@mail.fr")

    def test_get_step_should_return_step(self):
        user = create_user("user1@mail.fr")
        trip = create_trip(get_trip_object(name="trip", creator=user))
        start_datetime = "2020-04-10 21:00:00"
        created_step = create_step(get_step_object(name="step", trip_id=trip.id, start_datetime=start_datetime))
        step = get_step(created_step.id)
        self.assertIsInstance(step, Step)

    def test_get_uncreated_step_should_return_none(self):
        user = create_user("user1@mail.fr")
        trip = create_trip(get_trip_object(name="trip", creator=user))
        start_datetime = "2020-04-10 21:00:00"
        created_step = create_step(get_step_object(name="step", trip_id=trip.id, start_datetime=start_datetime))
        step = get_step(created_step.id + 1)
        self.assertEqual(step, None)

    def test_get_timeline_should_return_steps_ordered(self):
        user = create_user("user1@mail.fr")
        trip = create_trip(get_trip_object(name="trip", creator=user))
        created_step_1 = create_step(
            get_step_object(name="step", trip_id=trip.id, start_datetime="2020-04-10 21:00:00"))
        created_step_2 = create_step(
            get_step_object(name="step", trip_id=trip.id, start_datetime="2020-04-05 21:00:00"))
        timeline = get_timeline(trip.id)

        self.assertEqual(timeline[0].id, created_step_2.id)
        self.assertEqual(timeline[1].id, created_step_1.id)

    def test_get_timeline_should_raise_tripnotfoundexception(self):
        user = create_user("user1@mail.fr")
        trip = create_trip(get_trip_object(name="trip", creator=user))

        with self.assertRaises(TripNotFoundException):
            get_timeline(trip.id + 1)

    def test_get_timeline_should_return_participant_of_step(self):
        user1 = create_user("user1@mail.fr")
        user2 = create_user("user2@mail.fr")
        trip = create_trip(get_trip_object(name="trip", creator=user1))
        invite_to_trip(trip_id=trip.id, user_to_invite_email=user2.email)
        step = create_step(get_step_object(name="step", trip_id=trip.id, start_datetime="2020-05-04 22:22:00"))
        add_participant_to_step(user_id=user1.id, step_id=step.id)
        add_participant_to_step(user_id=user2.id, step_id=step.id)
        timeline = get_timeline(trip_id=trip.id)
        participants = [user1, user2]
        self.assertEqual(timeline[0].users_steps, participants)

    def test_get_finished_trips_should_raise_useridnotfoundexception(self):
        with self.assertRaises(UserIdNotFoundException):
            get_finished_trips_by_user(1)

    def test_get_finished_trips_should_return_finished_trips(self):
        user = create_user("user1@mail.fr")
        trips, closed_trips, ongoing_trips, coming_trips = get_preset_trips(user, datetime.date.today())
        self.assertEqual(get_finished_trips_by_user(user.id), closed_trips)

    def test_get_ongoing_trips_should_return_ongoing_trips(self):
        user = create_user("user1@mail.fr")
        today = datetime.date.today()
        trips, closed_trips, ongoing_trips, coming_trips = get_preset_trips(user, today)
        self.assertEqual(get_ongoing_trips_by_user(user.id, today), ongoing_trips)

    def test_get_ongoing_trips_should_raise_useridnotfoundexception(self):
        with self.assertRaises(UserIdNotFoundException):
            get_ongoing_trips_by_user(1)

    def test_get_coming_trips_should_return_coming_trips(self):
        user = create_user("user1@mail.fr")
        today = datetime.date.today()
        trips, closed_trips, ongoing_trips, coming_trips = get_preset_trips(user, today)
        self.assertEqual(get_coming_trips_by_user(user.id, today), coming_trips)

    def test_get_coming_trips_should_raise_useridnotfoundexception(self):
        with self.assertRaises(UserIdNotFoundException):
            get_coming_trips_by_user(1)

    def test_get_coming_trip_should_return_countdown_6(self):
        user = create_user("user1@mail.fr")
        today = datetime.date.today()
        get_coming_trips(user, today + datetime.timedelta(days=5))
        service_coming_trips = get_coming_trips_by_user(user.id, today)
        self.assertEqual(6, service_coming_trips[0].countdown)

    def test_get_coming_trip_with_no_step_should_return_countdown_0(self):
        user = create_user("user1@mail.fr")
        today = datetime.date.today()
        get_coming_trips(user, today)
        service_coming_trips = get_coming_trips_by_user(user.id, today)
        self.assertEqual(0, service_coming_trips[2].countdown)

    def test_add_participant_to_step_should_add_user(self):
        user = create_user("user1@mail.fr")
        trip = create_trip(get_trip_object("trip", user))
        step = create_step(get_step_object("step", trip.id, "2020-05-03 10:00:00"))
        step = add_participant_to_step(user.id, step.id)
        self.assertTrue(user in step.users_steps)

    def test_add_participant_to_step_should_raise_stepnotfoundexception(self):
        user = create_user("user1@mail.fr")
        trip = create_trip(get_trip_object("trip", user))
        step = create_step(get_step_object("step", trip.id, "2020-05-03 10:00:00"))
        with self.assertRaises(StepNotFoundException):
            add_participant_to_step(user.id, step.id + 1)

    def test_add_participant_to_step_should_raise_userdoesnotparticipatetotrip(self):
        creator = create_user("user1@mail.fr")
        usurper = create_user("user2@mail.fr")
        trip = create_trip(get_trip_object("trip", creator))
        step = create_step(get_step_object("step", trip.id, "2020-05-03 10:00:00"))
        with self.assertRaises(UserDoesNotParticipatesToTrip):
            add_participant_to_step(usurper.id, step.id)

    def test_get_user_personal_timeline(self):
        user = create_user("user1@mail.fr")
        trip = create_trip(get_trip_object("trip", user))
        step = create_step(get_step_object("step", trip.id, "2020-05-03 10:00:00"))
        step2 = create_step(get_step_object("step2", trip.id, "2020-05-03 10:00:00"))
        step = add_participant_to_step(user.id, step.id)
        step2 = add_participant_to_step(user.id, step2.id)
        expected_result = [step, step2]

        self.assertListEqual(get_user_steps_participation(user, trip.id), expected_result)

    def test_get_user_should_return_tripnotfoundexception(self):
        user = create_user("user1@mail.fr")
        with self.assertRaises(TripNotFoundException):
            get_user_steps_participation(user, 5)

    def test_create_expense(self):
        user = create_user("user1@mail.fr")
        trip = create_trip(get_trip_object("trip", user))
        expense = create_expense(get_expense_object(150.50, user.id, trip.id))
        self.assertIsInstance(expense, Expense)

    def test_create_reimbursement(self):
        user = create_user("user1@mail.fr")
        user2 = create_user("user2@mail.fr")
        trip = create_trip(get_trip_object("trip", user))
        expense = create_expense(get_expense_object(150.50, user.id, trip.id))
        reimbursement = create_reimbursement(get_reimbursement_object(100.50, expense.id, user.id, user2.id, trip.id))
        self.assertIsInstance(reimbursement, Reimbursement)

    def test_calculate_future_operations(self):
        user = create_user("user1@mail.fr")
        user2 = create_user("user2@mail.fr")
        user3 = create_user("user3@mail.fr")
        trip = create_trip(get_trip_object("trip", user))
        expense = create_expense(get_expense_object(150.50, user.id, trip.id))
        reimbursement = create_reimbursement(get_reimbursement_object(100, expense.id, user.id, user2.id, trip.id))
        reimbursement2 = create_reimbursement(get_reimbursement_object(100, expense.id, user.id, user2.id, trip.id))
        reimbursement3 = create_reimbursement(get_reimbursement_object(100, expense.id, user3.id, user.id, trip.id))
        operations = calculate_future_operations(refunds_to_get_for_user(trip.id, user.id),
                                                 get_user_reimbursements(trip.id, user.id))
        expected_result = [Operation(amount=100, emitter_id=user3.id, payee_id=user.id),
                           Operation(amount=200, emitter_id=user.id, payee_id=user2.id)]

        self.assertEquals(operations[0].amount, expected_result[0].amount)
        self.assertEquals(operations[1].amount, expected_result[1].amount)
        self.assertEquals(operations[0].emitter_id, expected_result[0].emitter_id)
        self.assertEquals(operations[1].emitter_id, expected_result[1].emitter_id)
        self.assertEquals(operations[0].payee_id, expected_result[0].payee_id)
        self.assertEquals(operations[1].payee_id, expected_result[1].payee_id)


if __name__ == '__main__':
    unittest.main()
