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


class AuthDto:
    api = Namespace('auth', description='authentication related operations')
    user_auth = api.model('auth_details', {
        'email': fields.String(required=True, description='The email address'),
        'password': fields.String(required=True, description='The user password '),
    })


class FileDto:
    api = Namespace('File', description='File related operations')
    file = api.model('file', {
        'id': fields.String(required=False, description='File id as uuid'),
        'name': fields.String(required=True, description='File name'),
        'extension': fields.String(required=True, description='File extension'),
        'created_date': fields.DateTime(required=False, description='File creation date'),
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

    coming_trip = api.model('coming trip', {
        'id': fields.Integer(required=True, description='trip id'),
        'name': fields.String(required=True, description='trip name'),
        'picture_path': fields.String(required=False, description='trip picture path'),
        'creator_id': fields.Integer(required=True, description='creator id'),
        'countdown': fields.Integer(required=True, description='countdown'),
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
        'country': NullableString(required=False, description='country'),
        'city': NullableString(required=False, description='city'),
        'postcode': NullableString(required=False, description='postcode'),
        'name': NullableString(required=False, description='name, e.g. Rue de Rivoli'),
        'state': NullableString(required=False, description='state, e.g. Île-de-France'),
    })

    step = api.model('step', {
        'id': fields.Integer(required=False, description='Step id'),
        'trip_id': fields.Integer(required=False, description='Trip id'),
        'name': fields.String(required=True, description='Step name'),
        'start_datetime': fields.DateTime(required=True, description='Starting datetime'),
        'end_datetime': NullableDateTime(required=False, description='End datetime'),
        'start_address': NullableNested(place, required=False),
        'end_address': NullableNested(place, required=False),
        'phone_number': NullableString(required=False, description='Phone number'),
        'reservation_number': NullableString(required=False, description='Reservation number'),
        'transport_number': NullableString(required=False, description='Transport number'),
        'type': fields.String(required=True, description='Step type'),
        'notes': NullableString(required=False, description='Notes'),
        'users_steps': fields.List(fields.Nested(UserDto.user), required=False),
        'files': fields.List(fields.Nested(FileDto.file))
    })


class ChatMessageDto:
    api = Namespace('chat_message', description='Chat message related operations')
    chat_message = api.model('chat_message', {
        'id': fields.Integer(required=False, description='Chat message id'),
        'message': fields.String(required=True, description='Message content'),
        'trip_id': fields.Integer(required=False, description='Trip id'),
        'user_id': fields.Integer(required=False, description='User id')
    })
