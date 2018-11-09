from flask import jsonify
from flask_restful import Resource
from . import api, api_rest  # noqa: F401
from ..models import Call as CallRecord
from .schemas import calls_schema


class Calls(Resource):
    def get(self):
        records = calls_schema.dump(CallRecord.query.all())
        return jsonify(records)

    def post(self):
        pass


class Call(Resource):
    def get(self, id):
        pass

    def delete(self, id):
        pass

    def put(self, id):
        pass


api_rest.add_resource(Calls, '/calls')
api_rest.add_resource(Call, '/calls/<int:id>')
