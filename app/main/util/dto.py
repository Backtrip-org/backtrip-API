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