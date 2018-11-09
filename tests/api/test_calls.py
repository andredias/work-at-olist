import pytest
from datetime import datetime
from app.models import Call


@pytest.fixture
def populate(db):
    Call.create(call_id=1, start_id=1, source='12345678901', destination='123456789', start_timestamp=datetime.now())
    Call.create(call_id=2, start_id=2, source='23456789012', destination='234567891', start_timestamp=datetime.now(), end_id=1, end_timestamp=datetime.now())


def test_calls_get(client, populate):
    response = client.get('/api/v1/calls')

    assert response.status_code == 200
    assert len(response.json) == 3
