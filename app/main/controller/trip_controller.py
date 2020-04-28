from flask import request
from flask_restplus import Resource

from app.main.model.step import Step
from ..model.trip import Trip
from ..service.auth_helper import Auth
from ..util.decorator import token_required, admin_token_required, user_token_required
from ..util.dto import TripDto
from ..service.trip_service import create_trip, create_step, invite_to_trip, get_step, get_timeline, user_participates_in_trip
from ..util.exception.TripException import TripAlreadyExistsException, TripNotFoundException
from ..util.exception.GlobalException import StringTooLongException
from ..util.exception.UserException import UserEmailNotFoundException

api = TripDto.api
_trip = TripDto.trip
_step = TripDto.step


@api.route('/')
class TripList(Resource):
    @api.doc('create a new trip')
    @api.expect(_trip, validate=True)
    @api.marshal_with(_trip)
    @api.response(201, 'Trip successfully created.')
    @api.response(401, 'Unknown access token.')
    @api.response(409, 'Trip already exist.')
    @token_required
    def post(self):
        try:
            trip_dto = request.json
            response, status = Auth.get_logged_in_user(request)
            new_trip = Trip(
                name=trip_dto.get('name'),
                picture_path=trip_dto.get('picture_path'),
                creator_id=response.get('data').id,
                users_trips=[response.get('data')]
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
    @api.response(400, 'Name is too long.')
    @api.response(401, 'Unknown access token.')
    @api.response(404, 'Unknown trip.')
    @api.marshal_with(_step)
    @token_required
    def post(self, trip_id):
        step_dto = request.json
        new_step = Step(
            name=step_dto.get('name'),
            trip_id=trip_id,
            start_datetime=step_dto.get('start_datetime')
        )
        try:
            return create_step(step=new_step), 201
        except TripNotFoundException as e:
            api.abort(404, e.value)
        except StringTooLongException as e:
            api.abort(400, e.value)


@api.route("/<trip_id>/invite")
@api.param('trip_id', 'Identifier of the trip')
class TripInvitation(Resource):
    @api.doc('Invite someone to a trip')
    @api.response(204, 'User as been added to trip')
    @api.response(400, 'User email not found')
    @api.response(401, 'Unknown access token')
    @api.response(404, 'Trip not found')
    @token_required
    def post(self, trip_id):
        try:
            invite_to_trip(trip_id, request.json.get('email'))
            return '', 204
        except TripNotFoundException as e:
            api.abort(404, e.value)
        except UserEmailNotFoundException as e:
            api.abort(400, e.value)


@api.route('/<trip_id>/step/<step_id>')
@api.param('trip_id', 'Identifier of the trip')
@api.param('step_id', 'Identifier of the step')
class TripStepWithId(Resource):
    @api.doc('Get step in a trip')
    @api.marshal_with(_step)
    @api.response(200, 'Step detail.')
    @api.response(401, 'Unknown access token.')
    @api.response(404, 'Unknown step.')
    @token_required
    def get(self, trip_id, step_id):
        step = get_step(step_id)
        if not step:
            api.abort(404, 'Step not found')
        else:
            return step


@api.route('/<trip_id>/timeline')
@api.param('trip_id', 'Identifier of the trip')
class TripTimeline(Resource):
    @api.doc('Get trip timeline')
    @api.marshal_with(_step)
    @api.response(200, 'Timeline detail.')
    @api.response(401, 'Unknown access token.')
    @api.response(401, 'You cannot access this timeline.')
    @api.response(404, 'Unknown trip.')
    @token_required
    def get(self, trip_id):
        response, status = Auth.get_logged_in_user(request)
        try:
            if not user_participates_in_trip(response.get('data').id, trip_id):
                api.abort(401, 'You cannot access this timeline.')
            return get_timeline(trip_id), 200
        except TripNotFoundException as e:
            api.abort(404, e.value)
