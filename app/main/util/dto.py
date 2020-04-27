from flask_restplus import Namespace, fields


class UserDto:
    api = Namespace('user', description='user related operations')
    user = api.model('user', {
        'id': fields.Integer(required=False, description='user id'),
        'email': fields.String(required=True, description='user email address'),
        'firstname': fields.String(required=True, description='user firstname'),
        'lastname': fields.String(required=True, description='user lastname'),
        'password': fields.String(required=True, description='user password'),
        'picture_path': fields.String(required=False, description='user picture path')
    })


class AuthDto:
    api = Namespace('auth', description='authentication related operations')
    user_auth = api.model('auth_details', {
        'email': fields.String(required=True, description='The email address'),
        'password': fields.String(required=True, description='The user password '),
    })


class TripDto:
    api = Namespace('trip', description='trip related operations')
    trip = api.model('trip', {
        'id': fields.Integer(required=False, description='trip id'),
        'name': fields.String(required=True, description='trip name'),
        'picture_path': fields.String(required=False, description='trip picture path'),
        'creator_id': fields.Integer(required=False, description='creator id'),
        'users_trips': fields.List(fields.Nested(UserDto.user))
    })

    step = api.model('step', {
        'id': fields.Integer(required=False, description='Step id'),
        'trip_id': fields.Integer(required=False, description='Step name'),
        'name': fields.String(required=True, description='Step name'),
        'start_datetime': fields.DateTime(required=True, description='Starting datetime of the step')
    })
