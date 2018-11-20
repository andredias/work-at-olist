from marshmallow import Schema, fields, post_load, pre_dump

ISO8601 = '%Y-%m-%dT%H:%M:%SZ'


class CallStartEndSchema(Schema):
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


def get_duration(interval):
    '''
    calculate duration in hours, minutes and seconds of a timedelta interval
    '''
    seconds = interval.total_seconds()
    reference = 3600
    duration = []
    while reference > 0:
        duration.append(int(seconds // reference))
        seconds -= duration[-1] * reference
        reference //= 60
    return duration


class BillDetailSchema(Schema):
    call_start_date = fields.Date()
    call_start_time = fields.Time()
    duration = fields.String()
    destination = fields.String()
    price = fields.Number()

    @pre_dump
    def adjust_data(self, original):
        interval = (original.end_timestamp - original.start_timestamp)
        duration = get_duration(interval)
        return {
            'call_start_date': original.start_timestamp.date(),
            'call_start_time': original.start_timestamp.time(),
            'duration': '{}h{}min{}s'.format(*duration),
            'destination': original.destination,
            'price': original.price
        }


class BillSchema(Schema):
    subscriber = fields.String()
    period = fields.String()
    calls = fields.Nested(BillDetailSchema, many=True)


call_rec_schema = CallStartEndSchema()
bill_details_schema = BillDetailSchema(many=True)
