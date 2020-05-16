from app.main import db
from app.main.model.step.step import Step


class LodgingStep(Step):
    __tablename__ = 'step_lodging'
    id = db.Column(db.Integer, db.ForeignKey('step.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'lodging',
    }