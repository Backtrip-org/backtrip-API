from app.main import db
from app.main.model.step import Step
from app.main.model.trip import Trip
from app.main.util.exception.TripException import TripAlreadyExistsException, TripNotFoundException
from app.main.util.exception.GlobalException import StringLengthOutOfRangeException
from app.main.util.exception.UserException import UserEmailNotFoundException, UserIdNotFoundException
from .user_service import get_user_by_email, get_user

from datetime import date


def create_trip(trip):
    if not Trip.name_min_length <= len(trip.name) <= Trip.name_max_length:
        raise StringLengthOutOfRangeException('Name', Trip.name_min_length, Trip.name_max_length)

    existing_trip = Trip.query.filter_by(creator_id=trip.creator_id).filter_by(name=trip.name).first()
    if not existing_trip:
        save_changes(trip)
        return trip
    else:
        raise TripAlreadyExistsException()


def create_step(step):
    if not trip_exists(step.trip_id):
        raise TripNotFoundException(step.trip_id)

    if not Step.name_min_length <= len(step.name) <= Step.name_max_length:
        raise StringLengthOutOfRangeException('Name', Step.name_min_length, Step.name_max_length)

    save_changes(step)
    return step


def invite_to_trip(trip_id, user_to_invite_email):
    trip = get_trip_by_id(trip_id)
    if trip is None:
        raise TripNotFoundException(trip_id)
    user = get_user_by_email(user_to_invite_email)
    if user is None:
        raise UserEmailNotFoundException(user_to_invite_email)

    trip.users_trips.append(user)
    save_changes(trip)
    pass


def save_changes(data):
    db.session.add(data)
    db.session.commit()


def get_trip_by_id(trip_id):
    return Trip.query.filter_by(id=trip_id).first()


def trip_exists(trip_id):
    return get_trip_by_id(trip_id) is not None


def get_step(step_id):
    return Step.query.filter_by(id=step_id).first()


def get_timeline(trip_id):
    if not trip_exists(trip_id):
        raise TripNotFoundException(trip_id)
    return Step.query.filter_by(trip_id=trip_id).order_by(Step.start_datetime).all()


def user_participates_in_trip(user_id, trip_id):
    if not trip_exists(trip_id):
        raise TripNotFoundException(trip_id)

    return any(user.id == user_id for user in get_trip_by_id(trip_id).users_trips)


def get_finished_trips_by_user(user_id):
    user = get_user(user_id)
    if not user:
        raise UserIdNotFoundException(user_id)

    closed_trips = list(filter(lambda trip: trip.closed, user.users_trips))
    return closed_trips


def get_first_step_of_trip(trip):
    return Step.query.filter_by(trip_id=trip.id).order_by(Step.start_datetime).first()


def is_ongoing_trip(trip, current_date):
    first_step = get_first_step_of_trip(trip)
    if not first_step:
        return False

    if not trip.closed and current_date >= first_step.start_datetime.date():
        return True

    return False


def get_ongoing_trips(trips, current_date):
    ongoing_trips = list(filter(lambda trip: is_ongoing_trip(trip, current_date), trips))
    return ongoing_trips


def get_ongoing_trips_by_user(user_id, current_date=date.today()):
    user = get_user(user_id)
    if not user:
        raise UserIdNotFoundException(user_id)

    ongoing_trips = get_ongoing_trips(user.users_trips, current_date)
    return ongoing_trips


def is_coming_trip(trip, current_date):
    first_step = get_first_step_of_trip(trip)
    if not first_step:
        return False

    if not trip.closed and current_date < first_step.start_datetime.date():
        return True

    return False


def get_coming_trips(trips, current_date):
    coming_trips = list(filter(lambda trip: is_coming_trip(trip, current_date), trips))
    return coming_trips


def get_coming_trips_by_user(user_id, current_date=date.today()):
    user = get_user(user_id)
    if not user:
        raise UserIdNotFoundException(user_id)

    coming_trips = get_coming_trips(user.users_trips, current_date)
    return coming_trips
