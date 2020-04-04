from flask import request
from flask_restplus import Resource

from ..util.decorator import token_required, admin_token_required, user_token_required
from ..util.dto import UserDto
from ..service.user_service import create_user, get_all_users, get_a_user

api = UserDto.api
_user = UserDto.user


@api.route('/')
class UserList(Resource):
    @api.doc('list_of_registered_users')
    @api.marshal_list_with(_user, envelope='data')
    @admin_token_required
    def get(self):
        return get_all_users()

    @api.response(201, 'User successfully created.')
    @api.doc('create a new user')
    @api.expect(_user, validate=True)
    def post(self):
        data = request.json
        return create_user(data=data)


@api.route('/<user_id>')
@api.param('user_id', 'The User identifier')
@api.response(404, 'User not found.')
class User(Resource):
    @api.doc('get a user')
    @api.marshal_with(_user)
    @user_token_required
    def get(self, user_id):
        user = get_a_user(user_id)
        if not user:
            api.abort(404)
        else:
            return user
