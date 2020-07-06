from datetime import datetime, timedelta

from app.main import db
from app.main.model.place.place import Place
from app.main.model.step.step import Step
from app.main.model.step.step_type import StepType, get_transport_step_types
from app.main.model.trip import Trip
from app.main.model.user import User


def get_global_stats():
    return {
        'open_trips': Trip.query.filter_by(closed=False).count(),
        'closed_trips': Trip.query.filter_by(closed=True).count(),
        'created_steps': Step.query.count(),
        'users_number': User.query.count()
    }


def get_top_visited_countries(number: int):
    places = Place.query.filter(Place.country.isnot(None)).all()
    top = dict()
    for place in places:
        if place.country in top:
            top[place.country] += 1
        else:
            top[place.country] = 1

    top = sorted(top.items(), key=lambda x: x[1], reverse=True)[:number]

    return {
        'labels': [label for label, value in top],
        'values': [value for label, value in top]
    }


def get_daily_registration(number_of_days: int, end_date: datetime):
    end_date = end_date.replace(hour=0, minute=0, second=0, microsecond=0)
    start_date = (end_date - timedelta(days=number_of_days - 1))
    delta = timedelta(days=1)
    labels = []
    values = []
    while start_date <= end_date:
        labels.append(start_date.strftime("%d/%m"))
        values.append(User.query.filter(db.func.date(User.registered_on) == start_date).count())
        start_date += delta

    return {
        'labels': labels,
        'values': values
    }


def get_step_types_distribution():
    steps = Step.query.all()
    labels = ['Restaurant', 'Loisir', 'Logement', 'Transport', 'Autre']
    food = len(list(filter(lambda step: StepType.from_string(step.type) == StepType.Food, steps)))
    leisure = len(list(filter(lambda step: StepType.from_string(step.type) == StepType.Leisure, steps)))
    lodging = len(list(filter(lambda step: StepType.from_string(step.type) == StepType.Lodging, steps)))
    transport = len(list(filter(lambda step: StepType.from_string(step.type) in get_transport_step_types(), steps)))
    other = len(list(filter(lambda step: StepType.from_string(step.type) == StepType.Base, steps)))

    return {
        'labels': labels,
        'values': [food, leisure, lodging, transport, other]
    }
