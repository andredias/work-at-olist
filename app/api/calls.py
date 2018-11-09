from flask import jsonify
from . import api
from ..models import Call
from .schemas import calls_schema


@api.route('/calls', methods=['GET'])
def get_calls():
    records = calls_schema.dump(Call.query.all())
    return jsonify(records)


@api.route('/calls', methods=['POST'])
def post_call():
    pass


@api.route('/calls/<int:id>', methods=['GET'])
def get_call(id):
    pass


@api.route('/calls/<int:id>', methods=['PUT'])
def put_call(id):
    pass


@api.route('/calls/<int:id>', methods=['DELETE'])
def delete_call(id):
    pass
