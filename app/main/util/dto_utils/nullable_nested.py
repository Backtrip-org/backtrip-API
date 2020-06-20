from flask_restplus.fields import Nested


class NullableNested(Nested):
    def schema(self):
        schema = super(NullableNested, self).schema()
        del schema['$ref']
        ref = '#/definitions/{0}'.format(self.nested.name)

        if self.as_list:
            schema['type'] = 'array'
            schema['items'] = {'$ref': ref}
        elif any(schema.values()):
            anyOf = schema.get('anyOf', [])
            anyOf.append({'$ref': ref})
            anyOf.append({'$ref': {'type': ['object', 'null']}})
            schema['anyOf'] = anyOf

        else:
            schema['anyOf'] = [{'$ref': ref}, {'type': ['object', 'null']}]
        return schema
