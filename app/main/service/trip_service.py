from app.main import db
from app.main.model.step.step import Step
from app.main.model.trip import Trip
from app.main.model.file.file import File
from app.main.util.exception.TripException import TripAlreadyExistsException, TripNotFoundException
from app.main.util.exception.UserException import UserEmailNotFoundException, UserDoesNotParticipatesToTrip, \
    UserIdNotFoundException
from app.main.util.exception.GlobalException import StringLengthOutOfRangeException
from .rating_service import get_rating
from .user_service import get_user_by_email, get_user
from ..model.expense import Expense
from ..model.operation import Operation
from ..model.reimbursement import Reimbursement
from ..util.exception.ExpenseException import ExpenseNotFoundException
from ..model.step.step_transport import StepTransport
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


def add_ratings(step):
    if step.start_address is not None:
        step.start_address.rating = get_rating(step.start_address)

    if isinstance(step, StepTransport) and step.end_address is not None:
        step.end_address.rating = get_rating(step.end_address)


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


def create_reimbursement(reimbursement):
    expense = get_expense(reimbursement.expense_id)
    if not expense:
        raise ExpenseNotFoundException(reimbursement.expense_id)

    if not get_user(reimbursement.emitter_id):
        raise UserIdNotFoundException(reimbursement.emitter_id)

    save_changes(reimbursement)
    return reimbursement


def refunds_to_get_for_user(trip_id, payee_id):
    return Reimbursement.query.filter_by(trip_id=trip_id).filter_by(payee_id=payee_id).all()


def get_user_reimbursements(trip_id, emitter_id):
    return Reimbursement.query.filter_by(trip_id=trip_id).filter_by(emitter_id=emitter_id).all()


def calculate_future_operations(refunds_to_get, user_reimbursements):
    operations = []
    reimbursements_to_remove = []
    for reimbursement in refunds_to_get:
        operation = Operation(reimbursement.emitter_id, reimbursement.payee_id, reimbursement.cost)
        add_reimbursements_that_concern_operation(user_reimbursements, operation, reimbursements_to_remove)
        append_operation(operations, operation)
        remove_done_reimbursements(user_reimbursements, reimbursements_to_remove)

    add_reimbursements_that_doesnt_concern_any_operation(user_reimbursements, operations)
    switch_emitter_and_payee_because_of_negative_amount(operations)

    return operations


def add_reimbursements_that_concern_operation(user_reimbursements, operation, reimbursements_to_remove):
    for user_reimbursement in user_reimbursements:
        if operation.payee_id == user_reimbursement.emitter_id and operation.emitter_id == user_reimbursement.payee_id:
            operation.amount -= user_reimbursement.cost
            reimbursements_to_remove.append(user_reimbursement)


def append_operation(operations, operation):
    for ope in operations:
        if ope.emitter_id == operation.emitter_id and ope.payee_id == operation.payee_id:
            ope.amount += operation.amount
            return operations
    operations.append(operation)


def remove_done_reimbursements(user_reimbursements, reimbursements_to_remove):
    for reimbursementToRemove in reimbursements_to_remove:
        if reimbursementToRemove in user_reimbursements:
            user_reimbursements.remove(reimbursementToRemove)


def add_reimbursements_that_doesnt_concern_any_operation(user_reimbursements, operations):
    for user_reimbursement in user_reimbursements:
        operation = Operation(user_reimbursement.emitter_id, user_reimbursement.payee_id, user_reimbursement.cost)
        append_operation(operations, operation)


def switch_emitter_and_payee_because_of_negative_amount(operations):
    for operation in operations:
        if operation.amount < 0:
            operation.amount = abs(operation.amount)
            temp = operation.payee_id
            operation.payee_id = operation.emitter_id
            operation.emitter_id = temp


def close_trip(trip_id):
    trip = get_trip_by_id(trip_id)
    if trip is None:
        raise TripNotFoundException(trip_id)
    if trip.closed:
        return
    trip.close()
    save_changes(trip)


def save_changes(data):
    db.session.add(data)
    db.session.commit()
