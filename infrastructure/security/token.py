from datetime import datetime, timedelta
from http import HTTPStatus
from zoneinfo import ZoneInfo

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from settings import Settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='users/login')


def create_access_token(claims: dict) -> str:
    """Create a JWT access token with the given claims."""
    to_enconde = claims.copy()

    try:
        expire = datetime.now(ZoneInfo('UTC')) + timedelta(
            hours=int(Settings().JWT_EXPIRATION_TIME)  # type: ignore
        )
    except Exception as e:
        raise ValueError(f'Error calculating expiration time: {e}')

    algoritm = Settings().JWT_ALGORITHM  # type: ignore
    secret_key = Settings().JWT_SECRET_KEY  # type: ignore

    to_enconde.update({'exp': expire})

    enconded_jwt = jwt.encode(
        payload=to_enconde, key=secret_key, algorithm=algoritm
    )

    return enconded_jwt


def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    """Get the current user from the JWT token."""
    algoritm = Settings().JWT_ALGORITHM  # type: ignore
    secret_key = Settings().JWT_SECRET_KEY  # type: ignore

    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )

    try:
        payload = jwt.decode(token, key=secret_key, algorithms=[algoritm])
    except jwt.PyJWTError:
        raise credentials_exception

    if payload.get('sub') is None:
        raise credentials_exception

    return payload
