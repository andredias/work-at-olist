from marshmallow import post_dump
from .. import ma
from ..models import Call


ISO8601 = '%Y-%m-%dT%H:%M:%SZ'


class CallSchema(ma.ModelSchema):
    class Meta:
        model = Call

    @post_dump
    def mk_iso8601_timestamp(self, data):
        data['timestamp'] = data['timestamp'][:19] + 'Z'
        return data


call_schema = CallSchema()
calls_schema = CallSchema(many=True)
