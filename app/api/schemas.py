from .. import ma
from ..models import Call


class CallSchema(ma.ModelSchema):
    class Meta:
        model = Call


call_schema = CallSchema()
calls_schema = CallSchema(many=True)
