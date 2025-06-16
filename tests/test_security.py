from jwt import decode, encode
from fastapi_zero.security import create_access_token, ALGORITHM, SECRET_KEY


def test_jwt():
    data = {'test': 'test'}
    token = create_access_token(data)
    decoded = decode(token, SECRET_KEY, ALGORITHM)

    assert decoded['test'] == data['test'] 