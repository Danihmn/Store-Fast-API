from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from application.usecases.user import AuthenticateCommand, AuthenticateHandler
from infrastructure.dependency_injection.container import Container

router = APIRouter(prefix='/users')


@router.post('/login')
@inject
async def login_user(
    command: AuthenticateCommand,
    handler: Annotated[
        AuthenticateHandler,
        Depends(Provide[Container.user_authenticate_handler]),
    ],
):
    """
    Autentica um usuário e retorna um token de acesso.
    """
    return await handler.handle(command)
