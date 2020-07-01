from flask_restplus import Namespace, fields

from app.main.util.dto_utils.nullable_datetime import NullableDateTime
from app.main.util.dto_utils.nullable_nested import NullableNested
from app.main.util.dto_utils.nullable_string import NullableString


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
    stats = api.model('stats', {
        'trips_number': fields.Integer(required=True, description='Number of trips'),
        'steps_number': fields.Integer(required=True, description='Number of steps'),
        'countries_visited': fields.Integer(required=True, description='Countries visited'),
        'cities_visited': fields.Integer(required=True, description='Cities visited'),
    })


class AuthDto:
    api = Namespace('auth', description='authentication related operations')
    user_auth = api.model('auth_details', {
        'email': fields.String(required=True, description='email address'),
        'password': fields.String(required=True, description='user password '),
    })


class FileDto:
    api = Namespace('file', description='file related operations')
    file = api.model('file', {
        'id': fields.String(required=False, description='file id as uuid'),
        'name': fields.String(required=True, description='file name'),
        'extension': fields.String(required=True, description='file extension'),
        'type': fields.String(required=True, description='file type : Document or Photo)'),
        'created_date': fields.DateTime(required=False, description='file creation date'),
    })


class TripDto:
    api = Namespace('trip', description='trip related operations')
    trip = api.model('trip', {
        'id': fields.Integer(required=False, description='trip id'),
        'name': fields.String(required=True, description='trip name'),
        'picture_path': fields.String(required=False, description='trip picture path'),
        'creator_id': fields.Integer(required=False, description='creator id'),
        'closed': fields.Boolean(required=False, description='trip status'),
        'users_trips': fields.List(fields.Nested(UserDto.user))
    })

    coming_trip = api.model('coming trip', {
        'id': fields.Integer(required=True, description='trip id'),
        'name': fields.String(required=True, description='trip name'),
        'picture_path': fields.String(required=False, description='trip picture path'),
        'creator_id': fields.Integer(required=True, description='creator id'),
        'countdown': fields.Integer(required=True, description='countdown'),
        'closed': fields.Boolean(required=False, description='trip status'),
        'users_trips': fields.List(fields.Nested(UserDto.user))
    })

    coordinate = api.model('coordinate', {
        'id': fields.Integer(required=False, description='coordinate id'),
        'latitude': fields.Float(required=True, description='latitude'),
        'longitude': fields.Float(required=True, description='longitude'),
    })

    place = api.model('place', {
        'id': fields.Integer(required=False, description='place id'),
        'coordinates': fields.Nested(coordinate),
        'name': NullableString(required=False, description='name, e.g. Hotel Ritz'),
        'street': NullableString(required=False, description='street'),
        'house_number': NullableString(required=False, description='house number'),
        'country': NullableString(required=False, description='country'),
        'city': NullableString(required=False, description='city'),
        'postcode': NullableString(required=False, description='postcode'),
        'state': NullableString(required=False, description='state, e.g. Île-de-France'),
        'rating': fields.Float(required=False, description='place rating according to Yelp')
    })

    step = api.model('step', {
        'id': fields.Integer(required=False, description='step id'),
        'trip_id': fields.Integer(required=False, description='trip id'),
        'name': fields.String(required=True, description='step name'),
        'start_datetime': fields.DateTime(required=True, description='starting datetime'),
        'end_datetime': NullableDateTime(required=False, description='end datetime'),
        'start_address': NullableNested(place, required=False),
        'end_address': NullableNested(place, required=False),
        'phone_number': NullableString(required=False, description='phone number'),
        'reservation_number': NullableString(required=False, description='reservation number'),
        'transport_number': NullableString(required=False, description='transport number'),
        'type': fields.String(required=True, description='step type'),
        'notes': NullableString(required=False, description='notes'),
        'users_steps': fields.List(fields.Nested(UserDto.user), required=False, description='participants'),
        'files': fields.List(fields.Nested(FileDto.file), description='related files')
    })

    notes = api.model('notes', {
        'notes': fields.String(required=True, description='notes')
    })

    expense = api.model('expense', {
        'id': fields.Integer(required=False, description="Expense id"),
        'name': fields.String(required=True, description="Expense name"),
        'cost': fields.Float(required=True, description="Expense value"),
        'trip_id': fields.Integer(required=False, description='Trip id'),
        'user_id': fields.Integer(required=False, description='User id')
    })

    reimbursement = api.model('reimbursement', {
        'id': fields.Integer(required=False, description="Expense id"),
        'cost': fields.Float(required=True, description="Reimbursement value"),
        'expense_id': fields.Integer(required=False, description='Expense id'),
        'emitter_id': fields.Integer(required=False, description='Emitter id'),
        'payee_id': fields.Integer(required=False, description='Payee id'),
        'trip_id': fields.Integer(required=False, description='Trip id'),
    })

    operation = api.model('operation', {
        'amount': fields.Float(required=True, description="Amount value"),
        'emitter_id': fields.Integer(required=False, description='Emitter id'),
        'payee_id': fields.Integer(required=False, description='Payee id'),
    })


class ChatMessageDto:
    api = Namespace('chat_message', description='Chat message related operations')
    chat_message = api.model('chat_message', {
        'id': fields.Integer(required=False, description='Chat message id'),
        'message': fields.String(required=True, description='Message content'),
        'trip_id': fields.Integer(required=False, description='Trip id'),
        'user_id': fields.Integer(required=False, description='User id')
    })

