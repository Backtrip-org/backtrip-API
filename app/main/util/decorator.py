from functools import wraps
from flask import request
from flask import abort

from app.main.service.auth_helper import Auth


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

        admin = user.get('admin')
        if not admin:
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

        user_id = user.get('id')
        if user_id != int(kwargs.get('user_id')):
            abort(401, "Unauthorized, you can't access to this user.")

        return f(*args, **kwargs)

    return decorated
