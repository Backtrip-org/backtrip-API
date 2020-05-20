from flask_restplus import fields


class NullableString(fields.String):
    __schema_type__ = ['string', 'null']
    __schema_example__ = 'nullable string'