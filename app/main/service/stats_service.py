from app.main.model.step.step import Step
from app.main.model.trip import Trip
from app.main.model.user import User


def get_global_stats():
    return {
        'open_trips': Trip.query.filter_by(closed=False).count(),
        'closed_trips': Trip.query.filter_by(closed=True).count(),
        'created_steps': Step.query.count(),
        'users_number': User.query.count()
    }