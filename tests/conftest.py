import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session
from datetime import datetime
from fastapi_zero.app import app
from fastapi_zero.models import table_registry, User
from fastapi_zero.database import get_session
from contextlib import contextmanager
from sqlalchemy.pool import StaticPool


@pytest.fixture
def client(session):
    def fake_session():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = fake_session
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def session():
    engine = create_engine('sqlite:///:memory:', 
                           connect_args={"check_same_thread": False}, 
                           poolclass=StaticPool)
    
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


@pytest.fixture
def user(session):
    user = User(username='jose', email='jose@fastapi.com.br', password='123456')
    session.add(user)
    session.commit()
    session.refresh(user)
    return user