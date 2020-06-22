import sqlalchemy
from flask import request
from flask_restplus import Resource

from ..model.expense import Expense
from ..model.file.file_type import FileType
from ..model.reimbursement import Reimbursement
from ..model.step.step_factory import StepFactory
from ..model.trip import Trip
from ..service.auth_helper import Auth
from ..service.file_service import upload
from ..service.trip_service import create_trip, create_step, invite_to_trip, get_step, get_timeline, \
    get_user_steps_participation, add_participant_to_step, get_participants_of_step, \
    add_file_to_step, create_expense, create_reimbursement, refunds_to_get_for_user, get_user_reimbursements, \
    calculate_future_operations, add_ratings, close_trip
from ..util.decorator import token_required, trip_participant_required
from ..util.dto import TripDto, UserDto, FileDto, ExpenseDto
from ..util.exception.ExpenseException import ExpenseNotFoundException
from ..util.exception.FileException import FileNotFoundException, UploadFileNotFoundException
from ..util.exception.GlobalException import StringLengthOutOfRangeException
from ..util.exception.StepException import StepNotFoundException, UnknownStepTypeException
from ..util.exception.TripException import TripAlreadyExistsException, TripNotFoundException
from ..util.exception.UserException import UserEmailNotFoundException, UserDoesNotParticipatesToTrip, \
    UserIdNotFoundException

trip_api = TripDto.api
_trip = TripDto.trip
_step = TripDto.step

file_api = FileDto.api
_file = FileDto.file

user_api = UserDto.api
_user = UserDto.user

expense_api = ExpenseDto.api
_expense = ExpenseDto.expense
_reimbursement = ExpenseDto.reimbursement
_operation = ExpenseDto.operation


@trip_api.route('/')
class TripList(Resource):
    @trip_api.doc('create a new trip')
    @trip_api.expect(_trip, validate=True)
    @trip_api.marshal_with(_trip)
    @trip_api.response(201, 'Trip successfully created.')
    @trip_api.response(401, 'Unknown access token.')
    @trip_api.response(409, 'Trip already exist.')
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
            trip_api.abort(409, e.value)
        except StringLengthOutOfRangeException as e:
            trip_api.abort(400, e.value)


@trip_api.route('/<trip_id>/step')
@trip_api.param('trip_id', 'Identifier of the trip')
class TripStep(Resource):
    @trip_api.doc('Create a step in a trip')
    @trip_api.expect(_step, validate=True)
    @trip_api.response(201, 'Step successfully created.')
    @trip_api.response(400, 'Name is too long.')
    @trip_api.response(400, 'Step type is unknown.')
    @trip_api.response(401, 'Unknown access token.')
    @trip_api.response(401, 'User cannot access this trip.')
    @trip_api.response(404, 'Unknown trip.')
    @trip_api.marshal_with(_step)
    @token_required
    @trip_participant_required
    def post(self, trip_id):
        step_dto = request.json

        try:
            new_step = StepFactory().get(step_dto, trip_id)
            add_ratings(new_step)

            return create_step(step=new_step), 201
        except TripNotFoundException as e:
            trip_api.abort(404, e.value)
        except StringLengthOutOfRangeException as e:
            trip_api.abort(400, e.value)
        except UnknownStepTypeException as e:
            trip_api.abort(400, e.value)


@trip_api.route("/<trip_id>/invite")
@trip_api.param('trip_id', 'Identifier of the trip')
class TripInvitation(Resource):
    @trip_api.doc('Invite someone to a trip')
    @trip_api.response(204, 'User as been added to trip')
    @trip_api.response(400, 'User email not found')
    @trip_api.response(401, 'Unknown access token')
    @trip_api.response(401, 'User cannot access this trip.')
    @trip_api.response(404, 'Trip not found')
    @token_required
    @trip_participant_required
    def post(self, trip_id):
        try:
            invite_to_trip(trip_id, request.json.get('email'))
            return '', 204
        except TripNotFoundException as e:
            trip_api.abort(404, e.value)
        except UserEmailNotFoundException as e:
            trip_api.abort(400, e.value)


@trip_api.route('/<trip_id>/step/<step_id>')
@trip_api.param('trip_id', 'Identifier of the trip')
@trip_api.param('step_id', 'Identifier of the step')
class TripStepWithId(Resource):
    @trip_api.doc('Get step in a trip')
    @trip_api.marshal_with(_step)
    @trip_api.response(200, 'Step detail.')
    @trip_api.response(401, 'Unknown access token.')
    @trip_api.response(401, 'User cannot access this trip.')
    @trip_api.response(404, 'Unknown step.')
    @token_required
    @trip_participant_required
    def get(self, trip_id, step_id):
        step = get_step(step_id)
        if not step:
            trip_api.abort(404, 'Step not found')
        else:
            return step


@trip_api.route('/<trip_id>/timeline')
@trip_api.param('trip_id', 'Identifier of the trip')
class TripTimeline(Resource):
    @trip_api.doc('Get trip timeline')
    @trip_api.marshal_with(_step)
    @trip_api.response(200, 'Timeline detail.')
    @trip_api.response(401, 'Unknown access token.')
    @trip_api.response(401, 'User cannot access this trip.')
    @trip_api.response(404, 'Unknown trip.')
    @token_required
    @trip_participant_required
    def get(self, trip_id):
        try:
            return get_timeline(trip_id), 200
        except TripNotFoundException as e:
            trip_api.abort(404, e.value)


@trip_api.route('/<trip_id>/timeline/personal')
@trip_api.param('trip_id', 'The Trip identifier')
class UserStepsParticipation(Resource):
    @trip_api.doc('Get user steps participation')
    @trip_api.marshal_with(_step)
    @trip_api.response(200, 'Steps.')
    @trip_api.response(401, 'Unknown access token.')
    @trip_api.response(401, 'You cannot access this steps.')
    @trip_api.response(401, 'User cannot access this trip.')
    @trip_api.response(404, 'Unknown trip.')
    @trip_api.response(404, 'Unknown user.')
    @token_required
    @trip_participant_required
    def get(self, trip_id):
        user_data, status = Auth.get_logged_in_user(request)
        user = user_data.get('data')
        if not user:
            trip_api.abort(404, 'User not found.')
        else:
            try:
                return get_user_steps_participation(user, trip_id)
            except TripNotFoundException as e:
                trip_api.abort(404, e.value)


@trip_api.route('/<trip_id>/step/<step_id>/participant')
@trip_api.param('trip_id', 'Identifier of the trip')
@trip_api.param('step_id', 'Identifier of the step')
class StepParticipant(Resource):
    @trip_api.doc('Add participant to step')
    @trip_api.response(200, 'Participant successfully added.')
    @trip_api.response(401, 'Unknown access token.')
    @trip_api.response(401, 'User cannot access this trip.')
    @trip_api.response(404, 'Step not found.')
    @trip_api.marshal_with(_user)
    @token_required
    @trip_participant_required
    def post(self, trip_id, step_id):
        try:
            user_id = request.json.get('id')
            add_participant_to_step(user_id, step_id)
            return get_participants_of_step(step_id)
            # return '', 204
        except StepNotFoundException as e:
            trip_api.abort(404, e.value)
        except UserDoesNotParticipatesToTrip as e:
            print('Don\'t participate')
            trip_api.abort(401, e.value)


@file_api.route('/<trip_id>/step/<step_id>/document')
@file_api.param('trip_id', 'Identifier of the trip')
@file_api.param('step_id', 'Identifier of the step')
class StepDocument(Resource):
    @file_api.doc('Add document to step')
    @file_api.response(200, 'Document successfully added.')
    @file_api.response(401, 'Unknown access token.')
    @file_api.response(401, 'User cannot access this trip.')
    @file_api.response(404, 'Step not found.')
    @file_api.response(404, 'File not found.')
    @file_api.marshal_with(_file)
    @trip_participant_required
    @token_required
    def post(self, trip_id, step_id):
        try:
            file = upload(request.files, FileType.Document)
            add_file_to_step(file.id, step_id)
            return file
        except StepNotFoundException as e:
            file_api.abort(404, e.value)
        except FileNotFoundException as e:
            file_api.abort(404, e.value)
        except UploadFileNotFoundException as e:
            file_api.abort(400, e.value)


@file_api.route('/<trip_id>/step/<step_id>/photo')
@file_api.param('trip_id', 'Identifier of the trip')
@file_api.param('step_id', 'Identifier of the step')
class StepDocument(Resource):
    @file_api.doc('Add photo to step')
    @file_api.response(200, 'Photo successfully added.')
    @file_api.response(401, 'Unknown access token.')
    @file_api.response(404, 'Step not found.')
    @file_api.response(404, 'File not found.')
    @file_api.marshal_with(_file)
    @token_required
    def post(self, trip_id, step_id):
        try:
            file = upload(request.files, FileType.Photo)
            add_file_to_step(file.id, step_id)
            return file
        except StepNotFoundException as e:
            file_api.abort(404, e.value)
        except FileNotFoundException as e:
            file_api.abort(404, e.value)
        except UploadFileNotFoundException as e:
            file_api.abort(400, e.value)


@expense_api.route('/<trip_id>/expense')
@expense_api.param('trip_id', 'Identifier of the trip')
class UserExpense(Resource):
    @expense_api.doc('Create a user expense')
    @expense_api.response(401, 'Unknown access token.')
    @expense_api.response(404, 'Unknown trip.')
    @expense_api.response(404, 'Unknown user.')
    @expense_api.marshal_with(_expense)
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
            expense_api.abort(404, e.value)
        except UserIdNotFoundException as e:
            expense_api.abort(404, e.value)


@expense_api.route('/<trip_id>/reimbursement')
@expense_api.param('trip_id', 'Identifier of the trip')
class UserReimbursement(Resource):
    @expense_api.doc('Create a user reimbursement')
    @expense_api.response(401, 'Unknown access token.')
    @expense_api.response(404, 'Unknown expense.')
    @expense_api.response(404, 'Unknown user.')
    @expense_api.marshal_with(_reimbursement)
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
            expense_api.abort(404, e.value)
        except UserIdNotFoundException as e:
            expense_api.abort(404, e.value)

            
@expense_api.route('/<trip_id>/transactionsToBeMade/<user_id>')
@expense_api.param('trip_id', 'Identifier of the trip')
@expense_api.param('user_id', 'Identifier of the user')
class TransactionsToBeMade(Resource):
    @expense_api.doc('Transactions to be made for a specific user')
    @expense_api.response(401, 'Unknown access token.')
    @expense_api.response(404, 'Unknown user.')
    @expense_api.marshal_with(_operation)
    @token_required
    def get(self, trip_id, user_id):
        try:
            refunds_to_get = refunds_to_get_for_user(trip_id, user_id)
            user_reimbursements = get_user_reimbursements(trip_id, user_id)
            return calculate_future_operations(refunds_to_get, user_reimbursements)
        except UserIdNotFoundException as e:
            expense_api.abort(404, e.value)
        
        
@trip_api.route('/<trip_id>/close')
@trip_api.param('trip_id', 'Identifier of the trip')
class CloseTrip(Resource):
    @trip_api.doc('Close trip')
    @trip_api.response(200, 'Trip successfully closed')
    @trip_api.response(401, 'User cannot access this trip.')
    @trip_api.response(401, 'Unknown access token.')
    @trip_api.response(404, 'Unknown trip.')
    @token_required
    @trip_participant_required
    def patch(self, trip_id):
        try:
            close_trip(trip_id)
            return 'Trip successfully closed.', 200
        except TripNotFoundException as e:
            trip_api.abort(404, e.value)
