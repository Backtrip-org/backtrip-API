from app.main import db
from app.main.model.place.coordinate import Coordinate


class Place(db.Model):
    __tablename__ = "place"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    coordinates_id = db.Column(db.Integer, db.ForeignKey('coordinate.id'))
    country = db.Column(db.String(60), unique=False)
    city = db.Column(db.String(85), unique=False)
    postcode = db.Column(db.String(10), unique=False)
    name = db.Column(db.String(150), unique=False)
    state = db.Column(db.String(70), unique=False)

    coordinates = db.relationship('Coordinate')

    @staticmethod
    def from_json(place_dto):
        if place_dto is None:
            return None
        return Place(
            coordinates=Coordinate.from_json(place_dto.get('coordinate')),
            country=place_dto.get('country'),
            city=place_dto.get('city'),
            postcode=place_dto.get('postcode'),
            name=place_dto.get('name'),
            state=place_dto.get('state')
        )