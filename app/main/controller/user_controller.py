import datetime

from flask import request
from flask_restplus import Resource

from ..util.decorator import token_required, admin_token_required, user_token_required
from ..util.dto import UserDto
from ..util.dto import TripDto
from ..service.user_service import create_user, get_all_users, get_user
from ..model.user import User as UserModel
from ..util.exception.UserException import UserAlreadyExistsException

api = UserDto.api
_user = UserDto.user
_trip = TripDto.trip


@api.route('/')
class UserList(Resource):
    @api.doc('list_of_registered_users')
    @api.marshal_list_with(_user, envelope='data')
    @api.response(200, 'List of users.')
    @api.response(401, 'Unknown access token.')
    @admin_token_required
    def get(self):
        return get_all_users()

    @api.doc('create a new user')
    @api.expect(_user, validate=True)
    @api.response(201, 'User successfully created.')
    @api.response(409, 'User already exist.')
    def post(self):
        data = request.json
        new_user = UserModel(
            email=data.get('email'),
            firstname=data.get('firstname'),
            lastname=data.get('lastname'),
            password=data.get('password'),
            registered_on=datetime.datetime.utcnow()
        )
        try:
            return create_user(new_user=new_user)
        except UserAlreadyExistsException as e:
            api.abort(409, e.value)


@api.route('/<user_id>')
@api.param('user_id', 'The User identifier')
class User(Resource):
    @api.doc('get a user')
    @api.marshal_with(_user)
    @api.response(200, 'User detail.')
    @api.response(401, 'Unknown access token.')
    @api.response(404, 'User not found.')
    @user_token_required
    def get(self, user_id):
        user = get_user(user_id)
        if not user:
            api.abort(404, 'User not found.')
        else:
            return user


@api.route('/<user_id>/trips')
@api.param('user_id', 'The User identifier')
class UserTrips(Resource):
    @api.doc('list_of_user_trips')
    @api.marshal_list_with(_trip, envelope='data')
    @api.response(200, 'User trips.')
    @api.response(401, 'Unknown access token.')
    @api.response(404, 'User not found.')
    @user_token_required
    def get(self, user_id):
        user = get_user(user_id)
        if not user:
            api.abort(404, 'User not found.')
        else:
            return user.users_trips
