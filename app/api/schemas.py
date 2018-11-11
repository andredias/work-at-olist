from marshmallow import Schema, fields, post_load


ISO8601 = '%Y-%m-%dT%H:%M:%SZ'


class CallSchema(Schema):
    id = fields.Integer(required=True, data_key='call_id')
    rec_id = fields.Integer(required=True, data_key='id')
    source = fields.String()
    destination = fields.String()
    timestamp = fields.DateTime(format=ISO8601, required=True)
    type = fields.String(required=True)

    @post_load
    def del_rec_id(self, data):
        data[data['type'] + '_timestamp'] = data['timestamp']
        del data['timestamp']
        del data['rec_id']
        del data['type']
        return data


call_schema = CallSchema()
