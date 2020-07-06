from app.main import db
from app.main.model.file.file_type import FileType
from app.main.model.place.place import Place
from app.main.model.step.step_type import StepType
from app.main.model.steps_files import steps_files
from app.main.model.users_steps import users_steps


class Step(db.Model):
    __tablename__ = "step"

    name_min_length = 2
    name_max_length = 20
    notes_max_length = 200

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    trip_id = db.Column(db.Integer, db.ForeignKey('trip.id'))
    name = db.Column(db.String(name_max_length), nullable=False, unique=False)
    start_datetime = db.Column(db.DateTime, nullable=False)
    end_datetime = db.Column(db.DateTime)
    start_address_id = db.Column(db.Integer, db.ForeignKey('place.id'))
    phone_number = db.Column(db.String(15))
    notes = db.Column(db.String(notes_max_length))
    type = db.Column(db.String(15))

    start_address = db.relationship('Place')
    users_steps = db.relationship('User', secondary=users_steps)
    files = db.relationship('File', secondary=steps_files)

    __mapper_args__ = {
        'polymorphic_identity': StepType.Base.name,
        'polymorphic_on': type
    }

    def get_photos(self):
        return [file for file in self.files if file.type == FileType.Photo]

    def get_step_type(self):
        return StepType.f

    @staticmethod
    def from_json(dto, trip_id):
        return Step(
            name=dto.get('name'),
            trip_id=trip_id,
            start_datetime=dto.get('start_datetime'),
            end_datetime=dto.get('end_datetime'),
            start_address=Place.from_json(dto.get('start_address')),
            phone_number=dto.get('phone_number'),
            notes=dto.get('notes')
        )
