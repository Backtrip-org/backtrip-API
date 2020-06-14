from functools import wraps
from flask import request
from flask import abort

from app.main.service.auth_helper import Auth
from app.main.service.trip_service import user_participates_in_trip, trip_exists


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        data, status = Auth.get_logged_in_user(request)
        user = data.get('data')

        if not user:
            return data, status

        return f(*args, **kwargs)

    return decorated


def admin_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        data, status = Auth.get_logged_in_user(request)
        user = data.get('data')

        if not user:
            return data, status

        if not user.admin:
            abort(401, 'Unauthorized, admin token required.')

        return f(*args, **kwargs)

    return decorated


def user_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        data, status = Auth.get_logged_in_user(request)
        user = data.get('data')
        if not user:
            return data, status

        user_id = user.id
        if user_id != int(kwargs.get('user_id')):
            abort(401, "Unauthorized, you can't access this user.")

        return f(*args, **kwargs)

    return decorated


def trip_participant_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        data, status = Auth.get_logged_in_user(request)
        user = data.get('data')
        if not user:
            return data, status

        user_id = user.id
        trip_id = kwargs.get('trip_id')

        if not trip_exists(trip_id):
            abort(404, "Trip with id {} does not exist")

        if not user_participates_in_trip(user_id, trip_id):
            abort(401, "Unauthorized, you can't access this trip")

        return f(*args, **kwargs)

    return decorated
