from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select

from domain.entities.user import Users
from infrastructure.data.database import get_session
from infrastructure.security.security import is_valid_password

router = APIRouter(prefix='/users')


@router.post('/login')
def login_user(
    session=Depends(get_session),
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    user = session.scalar(
        select(Users).where(Users.email == form_data.username)
    )

    if not user or not is_valid_password(
        password=form_data.password, hashed_password=user.hashed_password
    ):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Invalid email or password',
        )
