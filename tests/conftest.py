import pytest

from olist import create_app, db as _db


@pytest.fixture
def app():
    app = create_app('testing')
    return app


@pytest.fixture
def db(app):
    _db.create_all()
    yield _db
    _db.session.remove()
    _db.drop_all()
