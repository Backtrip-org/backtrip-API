from app.main import db
from app.main.model.place.coordinate import Coordinate


class Place(db.Model):
    __tablename__ = "place"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    coordinates_id = db.Column(db.Integer, db.ForeignKey('coordinate.id'))
    name = db.Column(db.String(150))
    street = db.Column(db.String(150))
    house_number = db.Column(db.String(10))
    country = db.Column(db.String(60))
    city = db.Column(db.String(85))
    postcode = db.Column(db.String(10))
    state = db.Column(db.String(70))
    rating = db.Column(db.DECIMAL(3,2))
    coordinates = db.relationship('Coordinate')

    @staticmethod
    def from_json(place_dto):
        if place_dto is None:
            return None
        return Place(
            coordinates=Coordinate.from_json(place_dto.get('coordinate')),
            name=place_dto.get('name'),
            street=place_dto.get('street'),
            house_number=place_dto.get('house_number'),
            country=place_dto.get('country'),
            city=place_dto.get('city'),
            postcode=place_dto.get('postcode'),
            state=place_dto.get('state')
        )