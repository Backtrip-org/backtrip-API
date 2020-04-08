from app.main import db
from app.main.model.user import User
from app.main.util.exception.UserException import UserAlreadyExistsException


def create_user(new_user):
    user = User.query.filter_by(email=new_user.email).first()
    if not user:
        save_changes(new_user)
        return generate_token(new_user)
    else:
        raise UserAlreadyExistsException


def get_all_users():
    return User.query.all()


def get_user(id):
    return User.query.filter_by(id=id).first()


def save_changes(data):
    db.session.add(data)
    db.session.commit()


def generate_token(user):
    try:
        auth_token = user.encode_auth_token(user.id)
        response_object = {
            'id': user.id,
            'status': 'success',
            'message': 'Successfully registered.',
            'Authorization': auth_token.decode()
        }
        return response_object, 201
    except Exception as e:
        response_object = {
            'status': 'fail',
            'message': 'Some error occurred. Please try again.'
        }
        return response_object, 401
