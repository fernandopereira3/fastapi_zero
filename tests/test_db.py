from dataclasses import asdict
from fastapi_zero.models import User, table_registry
from tests.conftest import session
from sqlalchemy import create_engine, select

def test_create_user(session):
    with session:
        new_user = User(username='testuser', 
                        email='testuser@example.com',
                        password='testpassword'
                        )
        session.add(new_user)
        session.commit()

    user = session.scalar(select(User).where(User.username == 'testuser'))

    assert user.username == 'testuser'
    assert user.email == 'testuser@example.com'
