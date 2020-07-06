from collections import OrderedDict

from flask import session
from sqlalchemy import func

from app.main.model.place.place import Place
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


def get_top_5_visited_countries():
    places = Place.query.filter(Place.country.isnot(None)).all()
    top = dict()
    for place in places:
        if place.country in top:
            top[place.country] += 1
        else:
            top[place.country] = 1

    top = sorted(top.items(), key=lambda x: x[1], reverse=True)[:5]

    return {
        'labels': [label for label, value in top],
        'values': [value for label, value in top]
    }
