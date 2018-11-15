import json
import pytest
from datetime import datetime, timedelta
from app.models import Call, calc_price


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


def previous_month(date):
    if date.month > 1:
        return datetime(date.year, date.month - 1, 1)
    else:
        return datetime(date.year - 1, 12, 1)


@pytest.fixture
def populate_calls(db):

    now = datetime.now()
    now_01 = datetime(now.year, now.month, 1)
    prev_month = previous_month(now)
    prev_prev_month = previous_month(prev_month)
    id = 0

    # ---- Ligações do mês - 2

    id += 1
    date = prev_prev_month + timedelta(days=3, hours=5, minutes=50)
    Call.create(
        id=id,
        source='10987654321',
        destination='1122334455',
        start_timestamp=date,
        end_timestamp=date + timedelta(minutes=20, seconds=15),
    )

    id += 1
    date = prev_prev_month + timedelta(days=15, hours=12, minutes=30, seconds=30)
    Call.create(
        id=id,
        source='12345678901',
        destination='87654321',
        start_timestamp=date,
        end_timestamp=date + timedelta(minutes=20, seconds=15),
    )

    id += 1
    date = prev_prev_month + timedelta(days=16, hours=13, minutes=30, seconds=30)
    Call.create(
        id=id,
        source='23456789012',
        destination='3344556677',
        start_timestamp=date,
        end_timestamp=date + timedelta(minutes=20, seconds=15),
    )

    # ---- Ligações do mês - 1

    id += 1
    date = prev_month - timedelta(minutes=30, seconds=30)
    Call.create(
        id=id,
        source='12345678901',
        destination='2233445566',
        start_timestamp=date,
        end_timestamp=date + timedelta(minutes=45, seconds=15),
    )

    id += 1
    date = prev_month + timedelta(days=15, hours=5, minutes=50)
    Call.create(
        id=id,
        source='12345678901',
        destination='2233445566',
        start_timestamp=date,
        end_timestamp=date + timedelta(minutes=20, seconds=15),
    )

    id += 1
    date = prev_month + timedelta(days=1, hours=12, minutes=30, seconds=30)
    Call.create(
        id=id,
        source='12345678901',
        destination='7890123456',
        start_timestamp=date,
        end_timestamp=date + timedelta(minutes=30, seconds=15),
    )

    id += 1
    date = prev_month + timedelta(days=16, hours=13, minutes=30, seconds=30)
    Call.create(
        id=id,
        source='23456789012',
        destination='3344556677',
        start_timestamp=date,
        end_timestamp=date + timedelta(minutes=20, seconds=15),
    )

    # ---- Ligações do mês

    id += 1
    date = now_01 - timedelta(minutes=30, seconds=30)
    Call.create(
        id=id,
        source='12345678901',
        destination='4455667788',
        start_timestamp=date,
        end_timestamp=date + timedelta(minutes=40, seconds=25),
    )

    id += 1
    date = now_01 + timedelta(hours=5, minutes=50)
    Call.create(
        id=id,
        source='33445566778',
        destination='7890123456',
        start_timestamp=date,
        end_timestamp=date + timedelta(minutes=25, seconds=15),
    )

    id += 1
    date = now_01 + timedelta(days=15, hours=12, minutes=30, seconds=30)
    Call.create(
        id=id,
        source='12345678901',
        destination='7890123456',
        start_timestamp=date,
        end_timestamp=date + timedelta(minutes=31, seconds=15),
    )

    id += 1
    date = now_01 + timedelta(days=16, hours=13, minutes=30, seconds=30)
    Call.create(
        id=id,
        source='23456789012',
        destination='3344556677',
        start_timestamp=date,
        end_timestamp=date + timedelta(minutes=22, seconds=29),
    )


def test_get_bill_mes_anterior(client, populate_calls):
    date_ref = previous_month(datetime.now())
    resp = client.get(f'/api/v1/calls/12345678901/{date_ref.year}/{date_ref.month}')

    data = resp.json
    assert data['subscriber'] == '12345678901'
    assert data['period'] == f'{date_ref.year}-{date_ref.month:02}'
    assert len(data['calls']) == 3
    assert data['calls'][1] == {
        'call_start_date': f'{date_ref.year}-{date_ref.month}-02',
        'call_start_time': '12:30:30',
        'destination': '7890123456',
        'duration': '0h30min15s',
        'price': 3.06
    }


def test_get_bill(client, populate_calls):
    date_ref = previous_month(datetime.now())
    resp1 = client.get(f'/api/v1/calls/12345678901/{date_ref.year}/{date_ref.month}')
    resp2 = client.get('/api/v1/calls/12345678901', follow_redirects=True)

    assert resp1.data == resp2.data


def test_get_bill_dois_meses_atras(client, populate_calls):
    date_ref = previous_month(previous_month(datetime.now()))
    resp = client.get(f'/api/v1/calls/12345678901/{date_ref.year}/{date_ref.month}')
    data = resp.json

    assert resp.status_code == 200
    assert data['subscriber'] == '12345678901'
    assert data['period'] == f'{date_ref.year}-{date_ref.month:02}'
    assert len(data['calls']) == 1
    assert data['calls'][0] == {
        'call_start_date': '2018-09-16',
        'call_start_time': '12:30:30',
        'destination': '87654321',
        'duration': '0h20min15s',
        'price': 2.16
    }


def test_get_bill_mes_atual(client, populate_calls):
    now = datetime.now()
    resp = client.get(f'/api/v1/calls/12345678901/{now.year}/{now.month}')
    data = resp.json

    assert resp.status_code == 200
    assert data['subscriber'] == '12345678901'
    assert data['period'] == f'{now.year}-{now.month:02}'
    assert len(data['calls']) == 0


def test_get_bill_chamada_de_um_dia(client, db):
    Call.create(
        id=1,
        source='99988526423',
        destination='9933468278',
        start_timestamp=datetime(2018, 2, 28, 21, 57, 13),
        end_timestamp=datetime(2018, 3, 1, 22, 10, 56),
    )
    resp = client.get('/api/v1/calls/99988526423/2018/3')
    data = resp.json

    assert len(data['calls']) == 1
    assert data['calls'][0] == {
        'call_start_date': '2018-02-28',
        'call_start_time': '21:57:13',
        'destination': '9933468278',
        'duration': '24h13min43s',
        'price': 86.94
    }
