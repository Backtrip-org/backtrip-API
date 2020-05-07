import unittest

from app.main.model.chat_message import ChatMessage
from app.main.service.chat_message_service import save_message, get_messages
from app.main.service.trip_service import create_trip
from app.main.util.exception.TripException import TripNotFoundException
from app.test.base import BaseTestCase
from app.test.test_trip_service import create_user, get_trip_object


def get_chat_message_object(message, trip_id, user_id):
    return ChatMessage(
        message=message,
        trip_id=trip_id,
        user_id=user_id
    )


class MyTestCase(BaseTestCase):
    def test_get_messages_from_trip(self):
        user1 = create_user("user1@mail.fr")
        user2 = create_user("user2@mail.fr")
        trip = create_trip(get_trip_object(name="first_trip", creator_id=user1.id))
        message1 = save_message(get_chat_message_object("first", trip.id, user1.id))
        message2 = save_message(get_chat_message_object("second", trip.id, user1.id))
        message3 = save_message(get_chat_message_object("first", trip.id, user2.id))
        messages_array = [message1, message2, message3]

        messages = get_messages(trip.id)
        self.assertListEqual(messages, messages_array)

    def test_get_messages_with_bad_trip_id(self):
        with self.assertRaises(TripNotFoundException):
            get_messages(3)


if __name__ == '__main__':
    unittest.main()
