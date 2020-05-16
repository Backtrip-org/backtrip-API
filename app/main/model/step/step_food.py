from app.main import db
from app.main.model.step.step import Step


class FoodStep(Step):
    __tablename__ = 'step_food'
    id = db.Column(db.Integer, db.ForeignKey('step.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'food',
    }