from datetime import datetime

from app.main.service.stats_service import get_global_stats, get_top_visited_countries, get_daily_registration, \
    get_step_types_distribution, get_transport_step_types_distribution
from app.main.util.decorator import admin_token_required
from app.main.util.dto import StatsDto
from flask_restplus import Resource

api = StatsDto.api
_global_stats = StatsDto.global_stats
_stats = StatsDto.stats


@api.route('/global')
class GlobalStats(Resource):
    @api.doc('Get step in a trip')
    @api.marshal_with(_global_stats)
    @api.response(200, 'Global stats.')
    @api.response(401, 'Unknown access token.')
    @api.response(401, 'Admin only.')
    @admin_token_required
    def get(self):
        return get_global_stats()


@api.route('/topVisitedCountries')
class TopVisitedCountries(Resource):
    @api.doc('Get top 5 visited countries')
    @api.marshal_with(_stats)
    @api.response(200, 'Top 5 visited countries.')
    @api.response(401, 'Unknown access token.')
    @api.response(401, 'Admin only.')
    @admin_token_required
    def get(self):
        return get_top_visited_countries(5)


@api.route('/last10DaysDailyRegistration')
class DailyRegistration(Resource):
    @api.doc('Get last 10 days daily registration')
    @api.marshal_with(_stats)
    @api.response(200, 'Last 10 days daily registration.')
    @api.response(401, 'Unknown access token.')
    @api.response(401, 'Admin only.')
    @admin_token_required
    def get(self):
        return get_daily_registration(10, datetime.today())


@api.route('/stepTypesDistribution')
class StepTypesDistribution(Resource):
    @api.doc('Get step types distribution')
    @api.marshal_with(_stats)
    @api.response(200, 'Step types distribution.')
    @api.response(401, 'Unknown access token.')
    @api.response(401, 'Admin only.')
    @admin_token_required
    def get(self):
        return get_step_types_distribution()


@api.route('/transportStepTypesDistribution')
class TransportStepTypesDistribution(Resource):
    @api.doc('Get transport step types distribution')
    @api.marshal_with(_stats)
    @api.response(200, 'Transport step types distribution.')
    @api.response(401, 'Unknown access token.')
    @api.response(401, 'Admin only.')
    @admin_token_required
    def get(self):
        return get_transport_step_types_distribution()
