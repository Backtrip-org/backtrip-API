from app.main import db


class Coordinate(db.Model):
    __tablename__ = "coordinate"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    latitude = db.Column(db.DECIMAL(9,7))
    longitude = db.Column(db.DECIMAL(10, 7))

    @staticmethod
    def from_json(coordinate_dto):
        if coordinate_dto is None:
            return None
        return Coordinate(
            id=coordinate_dto.get('id'),
            latitude=coordinate_dto.get('latitude'),
            longitude=coordinate_dto.get('longitude')
        )