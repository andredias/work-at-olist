from flask import jsonify
from flask_restful import Resource, reqparse
from itertools import chain
from . import api, api_rest  # noqa: F401
from ..models import Call as CallRecord
from .schemas import calls_schema

parser = reqparse.RequestParser()
parser.add_argument('id', type=int)


def _split_calls(record):
    start_call = {
        'call_id': record['call_id'],
        'id': record['start_id'],
        'type': 'start',
        'timestamp': record['start_timestamp'],
        'call_id': record['id'],
        'source': record['source'],
        'destination': record['destination'],
    } if record['start_id'] else None
    end_call = {
        'call_id': record['call_id'],
        'id': record['end_id'],
        'type': 'end',
        'timestamp': record['end_timestamp'],
        'call_id': record['id'],
    } if record['end_id'] else None
    return start_call, end_call


class Calls(Resource):
    def get(self):
        records = calls_schema.dump(CallRecord.query.all()).data
        records = (_split_calls(record) for record in records)
        records = chain(*records)
        records = [rec for rec in records if rec is not None]
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
