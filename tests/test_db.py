from dataclasses import asdict
from fastapi_zero.models import User
from sqlalchemy import select, event


def test_create_user(session, mock_db_time):
    new_user = User(username='testuser', email='testuser@example.com')
    session.add(new_user)
    session.commit()

    user = session.scalar(select(User).where(User.username == 'testuser'))

    assert user.username == 'testuser'
    assert user.email == 'testuser@example.com'
