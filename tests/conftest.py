import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session
from datetime import datetime
from fastapi_zero.app import app
from fastapi_zero.models import table_registry, User
from contextlib import contextmanager


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def session():
    engine = create_engine('sqlite:///:memory:')
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)


@contextmanager
def _mock_db_time(model, time=datetime(2025, 1, 1)):
    def fake_time_hook(mappper, connection, target):
        print(target)

    event.listen(User, 'before_insert', fake_time_hook)
    yield time
    event.remove(User, 'before_insert', fake_time_hook)
