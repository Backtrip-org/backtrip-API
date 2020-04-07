from flask import request
from flask_restplus import Resource

from ..model.trip import Trip
from ..service.auth_helper import Auth
from ..util.decorator import token_required, admin_token_required, user_token_required
from ..util.dto import TripDto
from ..service.trip_service import create_trip
from ..util.exception.TripException import TripAlreadyExistsException

api = TripDto.api
_trip = TripDto.trip


@api.route('/')
class TripList(Resource):
    @api.response(201, 'Trip successfully created.')
    @api.doc('create a new trip')
    @api.expect(_trip, validate=True)
    @api.marshal_with(_trip)
    @token_required
    def post(self):
        try:
            trip_dto = request.json
            response, status = Auth.get_logged_in_user(request)
            new_trip = Trip(
                name=trip_dto['name'],
                picture_path=trip_dto['picture_path'],
                creator_id=response.get('data').get('id')
            )
            return create_trip(trip=new_trip)
        except TripAlreadyExistsException as e:
            api.abort(409, e.value)

