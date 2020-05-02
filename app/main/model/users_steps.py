from .. import db

users_steps = db.Table(
    'users_steps',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('step_id', db.Integer, db.ForeignKey('step.id'), primary_key=True)
)
