from flask import request
from flask_restplus import Resource

from app.main.model.step import Step
from ..model.trip import Trip
from ..service.auth_helper import Auth
from ..util.decorator import token_required, admin_token_required, user_token_required
from ..util.dto import TripDto
from ..service.trip_service import create_trip, create_step, trip_exists
from ..util.exception.TripException import TripAlreadyExistsException

api = TripDto.api
_trip = TripDto.trip
_step = TripDto.step


@api.route('/')
class TripList(Resource):
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
            return create_trip(trip=new_trip), 201
        except TripAlreadyExistsException as e:
            api.abort(409, e.value)


@api.route('/<trip_id>/step')
@api.param('trip_id', 'Identifier of the trip')
class TripStep(Resource):
    @api.doc('Create a step in a trip')
    @api.expect(_step, validate=True)
    @api.response(201, 'Step successfully created.')
    @api.response(401, 'Unknown access token.')
    @api.response(404, 'Unknown trip.')
    @api.marshal_with(_step)
    @token_required
    def post(self, trip_id):
        if not trip_exists(trip_id):
            api.abort(404, 'Trip with id {} does not exists.'.format(str(trip_id)))

        step_dto = request.json
        new_step = Step(
            name=step_dto['name'],
            trip_id=trip_id,
            start_datetime=step_dto['start_datetime']
        )
        return create_step(step=new_step)

