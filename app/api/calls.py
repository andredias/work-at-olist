from datetime import datetime
from flask import jsonify, request
from marshmallow import ValidationError
from sqlalchemy import and_
from . import api
from .schemas import call_rec_schema, bill_details_schema
from ..models import Call


@api.route('/calls', methods=['POST'])
def create_call():
    '''
    Receive a start/end call record
    ---
    description: Receive a start/end call record
    parameters:
        - in: body
          name: start/end call record
          required: true
          schema:
              $ref: '#/definitions/StartEndCall'

    responses:
        200:
            description: Success
        400:
            description: No input data provided
        422:
            description: Validation error
    '''
    data = request.json
    if not data:
        return jsonify({'message': 'No input data provided'}), 400
    try:
        data = call_rec_schema.load(data)
    except ValidationError as error:
        return jsonify(error.messages), 422
    call = Call.get_by_id(data['id'])
    if not call:
        call = Call.create(**data)
    else:
        call.update(**data)
    return jsonify({'message': 'Success'})


@api.route('/calls/<string:subscriber>', methods=['GET'])
@api.route('/calls/<string:subscriber>/<int:year>/<int:month>', methods=['GET'])
def get_bill(subscriber, year=None, month=None):
    '''
    Get the telephone bill
    ---
    description: Get the telephone bill
    parameters:
        - name: subscriber
          in: path
          required: true
          type: string
        - in: path
          name: year
          type: integer
        - in: path
          name: month
          type: integer

    responses:
        200:
            description: Success
            schema:
                $ref: '#/definitions/Bill'

        204:
            description: No telephone bill for this period
    '''
    now = datetime.now()
    if not(year and month):
        year, month = (now.year, now.month - 1) if now.month > 1 else (now.year - 1, 12)
    ref_date = datetime(year=year, month=month, day=1)
    next_month = datetime(year=year, month=month + 1, day=1) \
        if month < 12 else datetime(year=year + 1, month=1, day=1)
    if (year, month) < (now.year, now.month):
        calls = Call.query.filter(and_(Call.source == subscriber,
                                       Call.end_timestamp >= ref_date,
                                       Call.end_timestamp < next_month))\
                          .order_by(Call.start_timestamp).all()
    else:
        calls = []
    if not calls:
        return '', 204
    return jsonify({
        'subscriber': subscriber,
        'period': f'{year}-{month:02}',
        'calls': bill_details_schema.dump(calls)
    })
