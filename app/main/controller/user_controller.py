import datetime

import sqlalchemy
from flask import request
from flask_restplus import Resource

from ..model.file.file_type import FileType
from ..model.user import User as UserModel
from ..service.file_service import upload
from ..service.trip_service import get_finished_trips_by_user, get_ongoing_trips_by_user, get_coming_trips_by_user
from ..service.user_service import create_user, get_all_users, get_user_by_id, update_profile_picture, get_trip_stats, \
    get_all_user_information, delete_all_user_information
from ..util.decorator import admin_token_required, user_token_required, token_required
from ..util.dto import TripDto, FileDto
from ..util.dto import UserDto
from ..util.exception.FileException import FileNotFoundException, UploadFileNotFoundException
from ..util.exception.UserException import UserAlreadyExistsException, UserNotFoundException
from ..util.gdpr_dto import GDPRDto

api = UserDto.api
_user = UserDto.user
_stats = UserDto.stats
_trip = TripDto.trip
_coming_trip = TripDto.coming_trip
_step = TripDto.step
_file = FileDto.file
_GDPR_user_information = GDPRDto.GDPR


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
        picture_path = data.get('picture_path') if data.get('picture_path') != '' else sqlalchemy.null()
        new_user = UserModel(
            email=data.get('email'),
            firstname=data.get('firstname'),
            lastname=data.get('lastname'),
            password=data.get('password'),
            picture_path=picture_path,
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
    @token_required
    def get(self, user_id):
        user = get_user_by_id(user_id)
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
        user = get_user_by_id(user_id)
        if not user:
            api.abort(404, 'User not found.')
        else:
            return user.users_trips


@api.route('/<user_id>/trips/finished')
@api.param('user_id', 'The User identifier')
class UserTripsFinished(Resource):
    @api.doc('List of finished trips for the user')
    @api.marshal_with(_trip)
    @api.response(200, 'User finished trips.')
    @api.response(401, 'Unknown access token.')
    @api.response(401, 'Access token does not correspond to requested user')
    @user_token_required
    def get(self, user_id):
        return get_finished_trips_by_user(user_id)


@api.route('/<user_id>/trips/ongoing')
@api.param('user_id', 'The User identifier')
class UserTripsOngoing(Resource):
    @api.doc('List of ongoing trips for the user')
    @api.marshal_with(_trip)
    @api.response(200, 'User ongoing trips.')
    @api.response(401, 'Unknown access token.')
    @api.response(401, 'Access token does not correspond to requested user')
    @user_token_required
    def get(self, user_id):
        return get_ongoing_trips_by_user(user_id)


@api.route('/<user_id>/trips/coming')
@api.param('user_id', 'The User identifier')
class UserTripsComing(Resource):
    @api.doc('List of coming trips for the user')
    @api.marshal_with(_coming_trip)
    @api.response(200, 'User coming trips.')
    @api.response(401, 'Unknown access token.')
    @api.response(401, 'Access token does not correspond to requested user')
    @user_token_required
    def get(self, user_id):
        return get_coming_trips_by_user(user_id)


@api.route('/<user_id>/trips/stats')
@api.param('user_id', 'The User identifier')
class UserTripsStats(Resource):
    @api.doc('Trips stats for the user')
    @api.marshal_with(_stats)
    @api.response(200, 'User trip stats.')
    @api.response(404, 'User not found.')
    @api.response(401, 'Unknown access token.')
    @api.response(401, 'Access token does not correspond to requested user')
    @token_required
    def get(self, user_id):
        try:
            return get_trip_stats(user_id)
        except UserNotFoundException as e:
            api.abort(404, e.value)


@api.route('/<user_id>/profilePicture')
@api.param('user_id', 'The User identifier')
class ProfilePicture(Resource):
    @api.doc('Update profile picture')
    @api.response(200, 'Picture successfully added.')
    @api.response(401, 'Unknown access token.')
    @api.response(401, 'Access token does not correspond to requested user')
    @api.response(404, 'User not found.')
    @api.response(404, 'File not found.')
    @api.marshal_with(_file)
    @token_required
    @user_token_required
    def post(self, user_id):
        try:
            file = upload(request.files, FileType.Photo)
            update_profile_picture(file.id, user_id)
            return file
        except UserNotFoundException as e:
            api.abort(404, e.value)
        except FileNotFoundException as e:
            api.abort(404, e.value)
        except UploadFileNotFoundException as e:
            api.abort(400, e.value)


@api.route('/<user_id>/GDPR_all_user_information')
@api.param('user_id', 'The User identifier')
class GDPRUserInformation(Resource):
    @api.doc('Get profile picture')
    @api.marshal_with(_GDPR_user_information)
    @api.response(200, 'User trip stats.')
    @api.response(404, 'User not found.')
    @api.response(401, 'Unknown access token.')
    @api.response(401, 'Access token does not correspond to requested user')
    @token_required
    def get(self, user_id):
        try:
            return get_all_user_information(user_id)
        except UserNotFoundException as e:
            api.abort(404, e.value)

    def delete(self, user_id):
        try:
            return delete_all_user_information(user_id)
        except UserNotFoundException as e:
            api.abort(404, e.value)
