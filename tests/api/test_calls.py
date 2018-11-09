import pytest
from datetime import datetime, timedelta
from app.models import Call
from app.api.schemas import calls_schema


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
    assert calls_schema.dump(Call.query.all()).data == response.json
