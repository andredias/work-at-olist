from flask import jsonify, request, url_for
from . import api
from ..models import Call
from .schemas import call_schema, calls_schema
from marshmallow import ValidationError


@api.route('/calls', methods=['GET'])
def get_calls():
    records = calls_schema.dump(Call.query.all())
    return jsonify(records)


@api.route('/calls', methods=['POST'])
def create_call():
    data = request.json
    if not data:
        return jsonify({'message': 'No input data provided'}), 400
    try:
        call = call_schema.load(data)
    except ValidationError as error:
        return jsonify(error.messages), 422
    if Call.get_by_id(call.id):
        return jsonify({'message': 'There is already a call with this id'}), 409
    call.save()
    return jsonify({'call': url_for('api.get_call', id=call.id)}), 201


@api.route('/calls/<int:id>', methods=['GET'])
def get_call(id):
    pass


@api.route('/calls/<int:id>', methods=['PUT'])
def put_call(id):
    pass


@api.route('/calls/<int:id>', methods=['DELETE'])
def delete_call(id):
    pass
