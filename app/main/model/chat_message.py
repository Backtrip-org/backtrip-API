from .. import db


class ChatMessage(db.Model):
    __tablename__ = "chat_message"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    message = db.Column(db.String(255), unique=False)
    trip_id = db.Column(db.Integer, db.ForeignKey('trip.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
