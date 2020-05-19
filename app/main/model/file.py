from .. import db
from sqlalchemy.sql import func


class File(db.Model):
    __tablename__ = "file"
    id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(255), unique=False)
    extension = db.Column(db.String(10), unique=False)
    created_date = db.Column(db.DateTime(timezone=True), server_default=func.now())
