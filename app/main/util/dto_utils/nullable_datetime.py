from flask_restplus import fields


class NullableDateTime(fields.DateTime):
    __schema_type__ = ['string', 'null']
    __schema_example__ = 'nullable datetime'