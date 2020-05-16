from .. import db

steps_files = db.Table(
    'steps_files',
    db.Column('step_id', db.Integer, db.ForeignKey('step.id'), primary_key=True),
    db.Column('file_id', db.String(50), db.ForeignKey('file.id'), primary_key=True)
)
