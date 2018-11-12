from marshmallow import Schema, fields, post_load, post_dump
from .. import ma
from ..models import Call

ISO8601 = '%Y-%m-%dT%H:%M:%SZ'


class CallSchema(Schema):
    id = fields.Integer(required=True, data_key='call_id')
    rec_id = fields.Integer(required=True, data_key='id')
    source = fields.String()
    destination = fields.String()
    timestamp = fields.DateTime(format=ISO8601, required=True)
    type = fields.String(required=True)

    @post_load
    def adjust_data(self, data):
        data[data['type'] + '_timestamp'] = data['timestamp']
        del data['timestamp']
        del data['rec_id']
        del data['type']
        return data


class BillSchema(ma.ModelSchema):
    class Meta:
        model = Call

    @post_dump(pass_original=True)
    def adjust_data(self, data, original):
        del data['id']
        del data['source']
        data['call_start_date'] = data['start_timestamp'][0:10]
        data['call_start_time'] = data['start_timestamp'][11:19]
        duration = str(original.end_timestamp - original.start_timestamp).split(':')
        data['duration'] = '{}h{}min{}s'.format(*duration)
        data['price'] = str(original.price)
        del data['start_timestamp']
        del data['end_timestamp']
        return data


call_schema = CallSchema()
bills_schema = BillSchema(many=True)
