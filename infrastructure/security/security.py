from pwdlib import PasswordHash

pwd_password = PasswordHash.recommended()


def hash_password(password: str) -> str:
    """Hash a password using the recommended hashing algorithm."""
    return pwd_password.hash(password)


def is_valid_password(password: str, hashed_password: str) -> bool:
    """Verify if a password matches the hashed password."""
    return pwd_password.verify(password, hashed_password)
