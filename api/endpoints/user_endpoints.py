import datetime
import uuid
from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select

from application.schemas.token_schema import TokenSchema
from application.schemas.user_schema import UserCreate, UserLogin
from domain.entities.user import Users
from infrastructure.data.database import get_session
from infrastructure.security.password import hash_password, is_valid_password
from infrastructure.security.token import create_access_token

router = APIRouter(prefix='/users')


@router.post(
    '/register',
    response_model=TokenSchema,
    status_code=HTTPStatus.CREATED,
)
def register_user(
    session=Depends(get_session),
    form_data: UserCreate = Depends(),
):
    user = session.scalar(select(Users).where(Users.email == form_data.email))

    if user:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='User with this email already exists',
        )

    new_user = Users(
        id=uuid.uuid4(),
        name=form_data.name,
        email=form_data.email,
        hashed_password=hash_password(form_data.hashed_password),
        role=form_data.role,
        active=form_data.active,
        created_at=datetime.datetime.now(),
        updated_at=datetime.datetime.now(),
    )

    session.add(new_user)
    session.commit()

    access_token = create_access_token(claims={'sub': new_user.email})

    return TokenSchema(access_token=access_token, token_type='Bearer')


@router.post('/login')
def login_user(
    session=Depends(get_session),
    form_data: UserLogin = Depends(),
):
    user = session.scalar(select(Users).where(Users.email == form_data.email))

    if not user or not is_valid_password(
        password=form_data.password, hashed_password=user.hashed_password
    ):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Invalid email or password',
        )

    access_token = create_access_token(claims={'sub': user.email})

    return TokenSchema(access_token=access_token, token_type='Bearer')
