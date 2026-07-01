import jwt

from infrastructure.security.token import create_access_token


def test_create_token():
    """Test the create_token function."""
    data = {'user_role': 'admin'}
    token = create_access_token(claims=data)

    assert token is not None
    assert isinstance(token, str)


def test_decode_token():
    """Test decoding the token to verify its contents."""
    data = {'user_role': 'admin'}
    token = create_access_token(claims=data)
    decoded_token = jwt.decode(token, options={'verify_signature': False})

    assert decoded_token['user_role'] == 'admin'
