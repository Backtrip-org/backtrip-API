from app.main import db
from app.main.model.trip import Trip
from app.main.util.exception.TripException import TripAlreadyExistsException


def create_trip(trip):
    existing_trip = Trip.query.filter_by(creator_id=trip.creator_id).filter_by(name=trip.name).first()
    if not existing_trip:
        save_changes(trip)
        return trip
    else:
        raise TripAlreadyExistsException()


def save_changes(data):
    db.session.add(data)
    db.session.commit()
