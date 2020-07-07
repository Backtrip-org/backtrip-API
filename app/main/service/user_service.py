from app.main import db
from app.main.model.file.file import File
from app.main.model.step.step import Step
from app.main.model.step.step_transport import StepTransport
from app.main.model.trip import Trip
from app.main.model.user import User
from app.main.service.file_service import get_file, delete
from app.main.util.exception.FileException import FileNotFoundException
from app.main.util.exception.UserException import UserAlreadyExistsException, UserNotFoundException


def create_user(new_user):
    user = User.query.filter_by(email=new_user.email).first()
    if not user:
        save_changes(new_user)
        return generate_token(new_user)
    else:
        raise UserAlreadyExistsException


def get_all_users():
    return User.query.all()


def get_user_by_id(id):
    return User.query.filter_by(id=id).first()


def get_user_by_email(email):
    return User.query.filter_by(email=email).first()


def generate_token(user):
    try:
        auth_token = user.encode_auth_token(user.id)
        response_object = {
            'id': user.id,
            'status': 'success',
            'message': 'Successfully registered.',
            'Authorization': auth_token.decode()
        }
        return response_object, 201
    except Exception as e:
        response_object = {
            'status': 'fail',
            'message': 'Some error occurred. Please try again.'
        }
        return response_object, 401


def get_trip_stats(user_id: int):
    user: User = get_user_by_id(user_id)
    if not user:
        raise UserNotFoundException(user_id)

    return {
        'trips_number': len(user.users_trips),
        'steps_number': len(user.users_steps),
        'countries_visited': count_countries(user.users_steps),
        'cities_visited': count_cities(user.users_steps)
    }


def count_countries(steps):
    countries = []
    for step in steps:
        if step.start_address is not None and step.start_address.country is not None:
            countries.append(step.start_address.country)
        if step is StepTransport and step.end_address is not None and step.end_address.country is not None:
            countries.append(step.end_address.country)
    return len(set(countries))


def count_cities(steps):
    cities = []
    for step in steps:
        if step.start_address is not None and step.start_address.city is not None:
            cities.append(step.start_address.city)
        if step is StepTransport and step.end_address is not None and step.end_address.city is not None:
            cities.append(step.end_address.city)
    return len(set(cities))


def update_profile_picture(file_id, user_id):
    user: User = get_user_by_id(user_id)
    if not user:
        raise UserNotFoundException(user_id)

    file: File = get_file(file_id)
    if not file:
        raise FileNotFoundException()

    if user.picture_path is not None:
        delete(user.picture_path)

    user.picture_path = file.id
    save_changes(user)


def ban(user_id):
    user = get_user_by_id(user_id)
    if user is None:
        raise UserNotFoundException(user_id)
    if user.banned:
        return
    user.ban()
    save_changes(user)


def save_changes(data):
    db.session.add(data)
    db.session.commit()
