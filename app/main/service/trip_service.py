from app.main import db
from app.main.model.step.step import Step
from app.main.model.trip import Trip
from app.main.model.file import File
from app.main.util.exception.TripException import TripAlreadyExistsException, TripNotFoundException
from app.main.util.exception.UserException import UserEmailNotFoundException, UserDoesNotParticipatesToTrip, \
    UserIdNotFoundException
from app.main.util.exception.GlobalException import StringLengthOutOfRangeException
from .user_service import get_user_by_email, get_user
from ..model.expense import Expense
from ..model.operation import Operation
from ..model.owe import Owe
from ..util.exception.ExpenseException import ExpenseNotFoundException
from ..util.exception.FileException import FileNotFoundException
from ..util.exception.StepException import StepNotFoundException
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


def get_expense(expense_id):
    return Expense.query.filter_by(id=expense_id).first()


def get_file(file_id):
    return File.query.filter_by(id=file_id).first()


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
    if trip.closed:
        return False

    first_step = get_first_step_of_trip(trip)
    if not first_step:
        return True

    if current_date < first_step.start_datetime.date():
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

    for trip in coming_trips:
        trip.countdown = get_countdown(trip, current_date)

    return coming_trips


def get_countdown(trip, current_date):
    first_step = get_first_step_of_trip(trip)

    if not first_step or trip.closed:
        return 0

    if current_date < first_step.start_datetime.date():
        return (first_step.start_datetime.date() - current_date).days

    return 0


def get_user_steps_participation(user, trip_id):
    if not trip_exists(trip_id):
        raise TripNotFoundException(trip_id)

    return list(filter(lambda step: step.trip_id == int(trip_id), user.users_steps))


def add_participant_to_step(user_id, step_id):
    step = get_step(step_id)
    if not step:
        raise StepNotFoundException(step_id)

    if not user_participates_in_trip(user_id, step.trip_id):
        raise UserDoesNotParticipatesToTrip(user_id, step.trip_id)

    user = get_user(user_id)
    step.users_steps.append(user)
    save_changes(step)
    return step


def get_participants_of_step(step_id):
    return Step.query.filter_by(id=step_id).first().users_steps


def add_file_to_step(file_id, step_id):
    step = get_step(step_id)
    if not step:
        raise StepNotFoundException(step_id)

    file = get_file(file_id)
    if not file:
        raise FileNotFoundException()

    step.files.append(file)
    save_changes(step)


def create_expense(expense):
    if not trip_exists(expense.trip_id):
        raise TripNotFoundException(expense.trip_id)

    if not get_user(expense.user_id):
        raise UserIdNotFoundException(expense.user_id)

    save_changes(expense)
    return expense


def create_owe(owe):
    expense = get_expense(owe.expense_id)
    if not expense:
        raise ExpenseNotFoundException(owe.expense_id)

    if not get_user(owe.emitter_id):
        raise UserIdNotFoundException(owe.emitter_id)

    save_changes(owe)
    return owe


def refunds_to_get_for_user(trip_id, payee_id):
    return Owe.query.filter_by(trip_id=trip_id).filter_by(payee_id=payee_id).all()


def get_user_owes(trip_id, emitter_id):
    return Owe.query.filter_by(trip_id=trip_id).filter_by(emitter_id=emitter_id).all()


def calculate_future_operations(refunds_to_get, user_owes):
    operations = []
    for owe in refunds_to_get:
        operation = Operation(owe.emitter_id, owe.payee_id, owe.cost)
        for user_owe in user_owes:
            if operation.payee_id == user_owe.emitter_id and operation.emitter_id == user_owe.payee_id:
                operation.amount -= user_owe.cost
                user_owes.remove(user_owe)
                break
        append_operation(operations, operation)

    for user_owe in user_owes:
        operation = Operation(user_owe.emitter_id, user_owe.payee_id, user_owe.cost)
        append_operation(operations, operation)

    return operations


def append_operation(operations, operation):
    for ope in operations:
        if ope.emitter_id == operation.emitter_id and ope.payee_id == operation.payee_id:
            ope.amount += operation.amount
            return operations
    operations.append(operation)
    return operations
