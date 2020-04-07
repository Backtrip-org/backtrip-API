from flask import request
from flask_restplus import Resource

from ..service.auth_helper import Auth
from ..util.decorator import token_required, admin_token_required, user_token_required
from ..util.dto import TripDto
from ..service.trip_service import create_trip

api = TripDto.api
_trip = TripDto.trip


@api.route('/')
class TripList(Resource):
    @api.response(201, 'Trip successfully created.')
    @api.doc('create a new trip')
    @api.expect(_trip, validate=True)
    @token_required
    def post(self):
        data = request.json
        response, status = Auth.get_logged_in_user(request)
        return create_trip(data=data, logged_in_user_id=response.get('data').get('id'))

