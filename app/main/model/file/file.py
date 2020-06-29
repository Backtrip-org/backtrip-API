import os

from app.main import db
from sqlalchemy.sql import func

from app.main.model.file.file_type import FileType


class File(db.Model):
    __tablename__ = "file"
    id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(255), unique=False)
    extension = db.Column(db.String(10), unique=False)
    type = db.Column(db.Enum(FileType), unique=False, nullable=False)
    created_date = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def get_path(self, directory_path):
        return os.path.join(directory_path, '{}.{}'.format(self.id, self.extension))
