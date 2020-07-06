from flask_restplus import Resource
from flask_socketio import emit

from app.init_app import socketIo, send, join_room
from ..model.chat_message import ChatMessage
from ..service.chat_message_service import get_messages, save_message
from ..util.decorator import token_required, trip_participant_required
from ..util.dto import ChatMessageDto
from ..util.exception.TripException import TripNotFoundException

api = ChatMessageDto.api
_chat_message = ChatMessageDto.chat_message


@api.route('/<trip_id>')
@api.param('trip_id', 'Identifier of the trip')
class ChatMessageList(Resource):
    @api.doc('get all messages')
    @api.marshal_with(_chat_message)
    @api.response(200, 'messages details.')
    @api.response(404, 'Messages not found.')
    @trip_participant_required
    @token_required
    def get(self, trip_id):
        try:
            return get_messages(trip_id), 200
        except TripNotFoundException as e:
            api.abort(404, e.value)


@socketIo.on('room_connection')
def connect_to_the_room(trip_id):
    join_room(trip_id)


@socketIo.on('message')
def chat_message(message, trip_id, user_id):
    new_message = ChatMessage(
        message=message,
        trip_id=trip_id,
        user_id=user_id,
    )
    saved_message = save_message(new_message)
    send({
        'id': saved_message.id,
        'message': saved_message.message,
        'trip_id': saved_message.trip_id,
        'user_id': saved_message.user_id
    }, room=trip_id)


@socketIo.on('isWriting')
def user_is_writing(user_id, trip_id):
    emit('isWriting', {'user_id': user_id}, room=trip_id)


@socketIo.on('stopWriting')
def user_stop_writing(user_id, trip_id):
    emit('stopWriting', {'user_id': user_id}, room=trip_id)
