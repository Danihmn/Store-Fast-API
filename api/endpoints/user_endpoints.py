from typing import Annotated

from fastapi import APIRouter, Depends

from application.usecases.user import AuthenticateCommand, AuthenticateHandler
from dependencies import get_user_authenticate_handler

router = APIRouter(prefix='/users')


@router.post('/login')
def login_user(
    command: AuthenticateCommand,
    handler: Annotated[
        AuthenticateHandler, Depends(get_user_authenticate_handler)
    ],
):
    """
    Authenticate a user and return an access token.
    """
    return handler.handle(command)
