import json
from datetime import datetime, timedelta
from app.models import Call
from app.api.calls import calc_price


def test_calc_price():
    now = datetime.now()
    d1 = datetime(now.year, now.month, now.day, 21, 57, 13)
    d2 = datetime(now.year, now.month, now.day, 22, 17, 53)
    assert calc_price(d1, d2) == 0.54

    d1 = datetime(now.year, now.month, now.day, 20, 57, 13)
    d2 = datetime(now.year, now.month, now.day, 21, 57, 53)
    assert calc_price(d1, d2) == 5.76

    d2 = datetime(now.year, now.month, now.day, 21, 57, 3)
    assert calc_price(d1, d2) == 5.67

    d2 = d1 + timedelta(hours=10)
    assert calc_price(d1, d2) == 11.07

    assert calc_price(None, None) is None
    assert calc_price(d1, None) is None
    assert calc_price(None, d2) is None


def test_create_call_1(client, db):
    now = datetime.now()

    data = {
        'id': 1,
        'call_id': 1,
        'destination': '123456789',
        'source': '12345678901',
        'timestamp': f'{now.year}-{now.month}-{now.day}T21:45:25Z',
        'type': 'start',
    }
    resp = client.post('/api/v1/calls', data=json.dumps(data),
                       content_type='application/json')
    assert resp.status_code == 200
    call = Call.get_by_id(1)
    assert call
    assert call.start_timestamp == datetime(now.year, now.month, now.day, 21, 45, 25)
    assert call.price is None
    assert call.end_timestamp is None

    data = {
        'id': 2,
        'call_id': 1,
        'timestamp': f'{now.year}-{now.month}-{now.day}T22:45:15Z',
        'type': 'end',
    }
    resp = client.post('/api/v1/calls', data=json.dumps(data),
                       content_type='application/json')
    assert resp.status_code == 200
    call = Call.get_by_id(1)
    assert call
    assert call.start_timestamp == datetime(now.year, now.month, now.day, 21, 45, 25)
    assert call.end_timestamp == datetime(now.year, now.month, now.day, 22, 45, 15)
    assert call.price is not None


def test_create_call_2(client, db):
    now = datetime.now()

    data = {
        'id': 1,
        'call_id': 1,
        'timestamp': f'{now.year}-{now.month}-{now.day}T22:45:15Z',
        'type': 'end',
    }
    resp = client.post('/api/v1/calls', data=json.dumps(data),
                       content_type='application/json')
    assert resp.status_code == 200
    call = Call.get_by_id(1)
    assert call
    assert call.end_timestamp == datetime(now.year, now.month, now.day, 22, 45, 15)
    assert call.price is None
    assert call.start_timestamp is None

    data = {
        'id': 2,
        'call_id': 1,
        'destination': '123456789',
        'source': '12345678901',
        'timestamp': f'{now.year}-{now.month}-{now.day}T21:45:25Z',
        'type': 'start',
    }
    resp = client.post('/api/v1/calls', data=json.dumps(data),
                       content_type='application/json')
    assert resp.status_code == 200
    call = Call.get_by_id(1)
    assert call
    assert call.start_timestamp == datetime(now.year, now.month, now.day, 21, 45, 25)
    assert call.end_timestamp == datetime(now.year, now.month, now.day, 22, 45, 15)
    assert call.price is not None


def test_create_invalid_call(client, db):
    data = {
        'id': 1,
        'call_id': 1,
        'destination': '123456789',
        'source': '12345678901',
        'timestamp': 'invalid',
        'type': 'start',
    }
    data['timestamp'] = 'invalid datetime'
    resp = client.post('/api/v1/calls', data=json.dumps(data),
                       content_type='application/json')
    assert resp.status_code == 422


def test_create_empty_call(client, db):
    resp = client.post('/api/v1/calls', data='{}',
                       content_type='application/json')
    assert resp == 400
