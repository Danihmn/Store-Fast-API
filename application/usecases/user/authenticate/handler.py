from http import HTTPStatus

from fastapi import HTTPException

from application.usecases.user.authenticate.command import Command
from application.usecases.user.authenticate.response import Response
from infrastructure.repositories.user_repository import UserRepository
from infrastructure.security.password import is_valid_password
from infrastructure.security.token import create_access_token


class Handler:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def handle(self, command: Command) -> Response:
        user = await self.repository.get_user_by_email(command.email)

        if not user or not is_valid_password(
            command.password, user.hashed_password
        ):
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail='Invalid credentials',
            )

        access_token = create_access_token(
            claims={
                'sub': str(user.id),
                'email': str(user.email),
                'name': str(user.name),
                'role': str(user.role),
            }
        )

        return Response(access_token=access_token, token_type='Bearer')
