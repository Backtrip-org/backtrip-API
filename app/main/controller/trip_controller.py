import sqlalchemy
from flask import request
from flask_restplus import Resource

from ..model.expense import Expense
from ..model.reimbursement import Reimbursement
from ..service.file_service import upload
from ..util.exception.ExpenseException import ExpenseNotFoundException
from ..util.exception.FileException import FileNotFoundException, UploadFileNotFoundException
from ..model.step.step_factory import StepFactory
from ..util.exception.StepException import StepNotFoundException, UnknownStepTypeException
from ..model.trip import Trip
from ..service.auth_helper import Auth
from ..util.decorator import token_required
from ..util.dto import TripDto, UserDto, FileDto, ExpenseDto, ReimbursementDto, OperationDto
from ..service.trip_service import create_trip, create_step, invite_to_trip, get_step, get_timeline, \
    user_participates_in_trip, get_user_steps_participation, add_participant_to_step, get_participants_of_step, \
    add_file_to_step, create_expense, create_reimbursement, refunds_to_get_for_user, get_user_reimbursements, calculate_future_operations
from ..util.exception.GlobalException import StringLengthOutOfRangeException
from ..util.exception.TripException import TripAlreadyExistsException, TripNotFoundException
from ..util.exception.UserException import UserEmailNotFoundException, UserDoesNotParticipatesToTrip, \
    UserIdNotFoundException

api = TripDto.api
_trip = TripDto.trip
_step = TripDto.step
_user = UserDto.user
_file = FileDto.file
_expense = ExpenseDto.expense
_reimbursement = ReimbursementDto.reimbursement
_operation = OperationDto.operation


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
            picture_path = trip_dto.get('picture_path') if trip_dto.get('picture_path') != '' else sqlalchemy.null()
            new_trip = Trip(
                name=trip_dto.get('name'),
                picture_path=picture_path,
                creator_id=response.get('data').id,
                users_trips=[response.get('data')],
                closed=False
            )
            return create_trip(trip=new_trip), 201
        except TripAlreadyExistsException as e:
            api.abort(409, e.value)
        except StringLengthOutOfRangeException as e:
            api.abort(400, e.value)


@api.route('/<trip_id>/step')
@api.param('trip_id', 'Identifier of the trip')
class TripStep(Resource):
    @api.doc('Create a step in a trip')
    @api.expect(_step, validate=True)
    @api.response(201, 'Step successfully created.')
    @api.response(400, 'Name is too long.')
    @api.response(400, 'Step type is unknown.')
    @api.response(401, 'Unknown access token.')
    @api.response(404, 'Unknown trip.')
    @api.marshal_with(_step)
    @token_required
    def post(self, trip_id):
        step_dto = request.json

        try:
            new_step = StepFactory(step_dto, trip_id).get()
            return create_step(step=new_step), 201
        except TripNotFoundException as e:
            api.abort(404, e.value)
        except StringLengthOutOfRangeException as e:
            api.abort(400, e.value)
        except UnknownStepTypeException as e:
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


@api.route('/<trip_id>/timeline/personal')
@api.param('trip_id', 'The Trip identifier')
class UserStepsParticipation(Resource):
    @api.doc('Get user steps participation')
    @api.marshal_with(_step)
    @api.response(200, 'Steps.')
    @api.response(401, 'Unknown access token.')
    @api.response(401, 'You cannot access this steps.')
    @api.response(404, 'Unknown trip.')
    @api.response(404, 'Unknown user.')
    @token_required
    def get(self, trip_id):
        user_data, status = Auth.get_logged_in_user(request)
        user = user_data.get('data')
        if not user:
            api.abort(404, 'User not found.')
        else:
            try:
                return get_user_steps_participation(user, trip_id)
            except TripNotFoundException as e:
                api.abort(404, e.value)


@api.route('/<trip_id>/step/<step_id>/participant')
@api.param('trip_id', 'Identifier of the trip')
@api.param('step_id', 'Identifier of the step')
class StepParticipant(Resource):
    @api.doc('Add participant to step')
    @api.response(200, 'Participant successfully added.')
    @api.response(401, 'Unknown access token.')
    @api.response(401, 'User cannot access this trip.')
    @api.response(404, 'Step not found.')
    @api.marshal_with(_user)
    @token_required
    def post(self, trip_id, step_id):
        try:
            user_id = request.json.get('id')
            add_participant_to_step(user_id, step_id)
            return get_participants_of_step(step_id)
            # return '', 204
        except StepNotFoundException as e:
            api.abort(404, e.value)
        except UserDoesNotParticipatesToTrip as e:
            print('Don\'t participate')
            api.abort(401, e.value)


@api.route('/<trip_id>/step/<step_id>/document')
@api.param('trip_id', 'Identifier of the trip')
@api.param('step_id', 'Identifier of the step')
class StepParticipant(Resource):
    @api.doc('Add document to step')
    @api.response(200, 'Document successfully added.')
    @api.response(401, 'Unknown access token.')
    @api.response(404, 'Step not found.')
    @api.response(404, 'File not found.')
    @api.marshal_with(_file)
    @token_required
    def post(self, trip_id, step_id):
        try:
            file = upload(request.files)
            add_file_to_step(file.id, step_id)
            return file
        except StepNotFoundException as e:
            api.abort(404, e.value)
        except FileNotFoundException as e:
            api.abort(404, e.value)
        except UploadFileNotFoundException as e:
            api.abort(400, e.value)


@api.route('/<trip_id>/expense')
@api.param('trip_id', 'Identifier of the trip')
class UserExpense(Resource):
    @api.doc('Create a user expense')
    @api.response(401, 'Unknown access token.')
    @api.response(404, 'Unknown trip.')
    @api.response(404, 'Unknown user.')
    @api.marshal_with(_expense)
    @token_required
    def post(self, trip_id):
        try:
            user_id = request.json.get('user_id')
            cost = request.json.get('cost')

            expense = Expense(
                cost=cost,
                user_id=user_id,
                trip_id=trip_id
            )

            return create_expense(expense)
        except TripNotFoundException as e:
            api.abort(404, e.value)
        except UserIdNotFoundException as e:
            api.abort(404, e.value)


@api.route('/<trip_id>/reimbursement')
@api.param('trip_id', 'Identifier of the trip')
class UserReimbursement(Resource):
    @api.doc('Create a user reimbursement')
    @api.response(401, 'Unknown access token.')
    @api.response(404, 'Unknown expense.')
    @api.response(404, 'Unknown user.')
    @api.marshal_with(_reimbursement)
    @token_required
    def post(self, trip_id):
        try:
            expense_id = request.json.get('expense_id')
            emitter_id = request.json.get('emitter_id')
            payee_id = request.json.get('payee_id')
            cost = request.json.get('cost')

            reimbursement = Reimbursement(
                cost=cost,
                emitter_id=emitter_id,
                expense_id=expense_id,
                payee_id=payee_id,
                trip_id=trip_id
            )

            return create_reimbursement(reimbursement)
        except ExpenseNotFoundException as e:
            api.abort(404, e.value)
        except UserIdNotFoundException as e:
            api.abort(404, e.value)


@api.route('/<trip_id>/transactionsToBeMade/<user_id>')
@api.param('trip_id', 'Identifier of the trip')
@api.param('user_id', 'Identifier of the user')
class TransactionsToBeMade(Resource):
    @api.doc('Transactions to be made for a specific user')
    @api.response(401, 'Unknown access token.')
    @api.response(404, 'Unknown user.')
    @api.marshal_with(_operation)
    @token_required
    def get(self, trip_id, user_id):
        try:
            refunds_to_get = refunds_to_get_for_user(trip_id, user_id)
            user_reimbursements = get_user_reimbursements(trip_id, user_id)
            return calculate_future_operations(refunds_to_get, user_reimbursements)
        except UserIdNotFoundException as e:
            api.abort(404, e.value)