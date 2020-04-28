from app.app import socketIo, send


@socketIo.on('message')
def chat_message(message):
    print(message)
    send(message, broadcast=True)
    return None
