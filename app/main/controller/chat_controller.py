from app.init_app import socketIo, send, join_room


@socketIo.on('room_connection')
def connect_to_the_room(trip_id):
    print(trip_id)
    join_room(trip_id)
    return None


@socketIo.on('message')
def chat_message(message, trip_id):
    print(trip_id)
    print(message)
    send(message, room=trip_id)
    return None
