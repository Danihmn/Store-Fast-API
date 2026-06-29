from infrastructure.security.security import hash_password, is_valid_password


def test_hash_password():
    """Test the hash_password function."""
    password = 'my_secure_password'
    hashed_password = hash_password(password)

    assert hashed_password is not None
    assert isinstance(hashed_password, str)
    assert hashed_password != password


def test_is_valid_password():
    password = 'my_secure_password'
    hashed_password = hash_password(password)

    assert is_valid_password(password, hashed_password) is True
    assert is_valid_password('wrong_password', hashed_password) is False
