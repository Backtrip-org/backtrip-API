from app.main.util.dto import TripDto, ChatMessageDto, FileDto, UserDto
from flask_restplus import Namespace, fields


class GDPRDto:
    api = Namespace('GDPR', description='GDPR related operations')
    GDPR = api.model('user', {
        'user': fields.Nested(UserDto.user),
        'trips': fields.List(fields.Nested(TripDto.trip), description='related trips'),
        'steps': fields.List(fields.Nested(TripDto.step), description='related steps'),
        'messages': fields.List(fields.Nested(ChatMessageDto.chat_message), description='related messages'),
        'expenses': fields.List(fields.Nested(TripDto.expense), description='related expenses'),
        'reimbursements': fields.List(fields.Nested(TripDto.reimbursement), description='related reimbursements')
    })
