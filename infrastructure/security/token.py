from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import jwt

from settings import Settings


def create_access_token(claims: dict) -> str:
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
