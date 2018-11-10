import json
import pytest
from datetime import datetime, timedelta
from app.models import Call
from app.api.schemas import call_schema, calls_schema


@pytest.fixture
def populate(db):
    Call.create(id=1, call_id=1, source='12345678901', destination='123456789',
                timestamp=datetime.now(), type='start')
    Call.create(id=2, call_id=2, source='23456789012', destination='234567891',
                timestamp=datetime.now() + timedelta(minutes=1), type='end')
    Call.create(id=3, call_id=1, timestamp=datetime.now() + timedelta(minutes=2),
                type='start')


def test_calls_get(client, populate):
    response = client.get('/api/v1/calls')

    assert response.status_code == 200
    assert len(response.json) == 3
    assert calls_schema.dump(Call.query.all()) == response.json


def test_iso8601_timestamp(db):
    c = Call.create(id=1, call_id=1, source='12345678901', destination='123456789',
                    timestamp=datetime(2018, 11, 9, 18, 36, 00), type='start')
    json = call_schema.dump(c)

    assert json['timestamp'] == '2018-11-09T18:36:00Z'


def test_create_call_1(client, db):
    data = {
        'id': 1,
        'call_id': 1,
        'destination': '123456789',
        'source': '12345678901',
        'timestamp': '2018-11-09T21:45:25Z',
        'type': 'start',
    }
    resp = client.post('/api/v1/calls', data=json.dumps(data),
                       content_type='application/json')

    assert resp.status_code == 201
    assert b'{"call":"/api/v1/calls/1"}\n' in resp.data
    call = Call.get_by_id(1)
    assert call
    assert call.timestamp == datetime(2018, 11, 9, 21, 45, 25)

    data['timestamp'] = '2018-11-09T21:54:00Z'
    resp = client.post('/api/v1/calls', data=json.dumps(data),
                       content_type='application/json')
    assert resp.status_code == 409


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


def test_get_start_call(client, db):
    Call.create(id=1, call_id=1, source='12345678901', destination='123456789',
                timestamp=datetime.now(), type='start')
    resp = client.get('/api/v1/calls/1')

    assert resp.status_code == 200
    data = json.loads(resp.data.decode('utf-8'))
    assert data and data['source'] and data['destination']


def test_get_end_call(client, db):
    Call.create(id=1, call_id=1, timestamp=datetime.now(), type='end')
    resp = client.get('/api/v1/calls/1')

    assert resp.status_code == 200
    data = json.loads(resp.data.decode('utf-8'))
    assert data and 'source' not in data and 'destination' not in data


def test_inexistent_call(client, db):
    resp = client.get('/api/v1/calls/10')

    assert resp.status_code == 404
