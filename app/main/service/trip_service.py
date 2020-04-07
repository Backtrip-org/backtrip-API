from app.main import db
from app.main.model.trip import Trip


def create_trip(data, logged_in_user_id):
    trip = Trip.query.filter_by(creator_id=logged_in_user_id).filter_by(name=data['name']).first()
    if not trip:
        new_trip = Trip(
            name=data['name'],
            picture_path=data['picture_path'],
            creator_id=logged_in_user_id
        )
        save_changes(new_trip)
        response_object = {
            'status': 'success',
            'message': 'Successfully created.'
        }
        return response_object, 201
    else:
        response_object = {
            'status': 'fail',
            'message': 'Trip already exists. Please choose a new name.',
        }
        return response_object, 409


def save_changes(data):
    db.session.add(data)
    db.session.commit()