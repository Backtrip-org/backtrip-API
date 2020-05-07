from app.main import db
from app.main.model.chat_message import ChatMessage
from app.main.service.trip_service import trip_exists
from app.main.util.exception.TripException import TripNotFoundException


def get_messages(trip_id):
    if not trip_exists(trip_id):
        raise TripNotFoundException(trip_id)
    return ChatMessage.query.filter_by(trip_id=trip_id).all()


def save_message(message):
    db.session.add(message)
    db.session.commit()
    return message
