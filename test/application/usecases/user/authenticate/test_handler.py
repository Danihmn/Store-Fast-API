from application.usecases.user.authenticate.command import Command
from application.usecases.user.authenticate.handler import Handler
from application.usecases.user.authenticate.response import Response
from infrastructure.repositories.user_repository import UserRepository
from test.configuration.fake_data import UserFactory


async def test_handler_authenticate_user_success(session):
    # arrange
    user = UserFactory.create()

    session.add(user)
    await session.commit()

    command = Command(email=user.email, password='hashed_password')
    handler = Handler(UserRepository(session))

    # act
    result = await handler.handle(command)

    # assert
    assert isinstance(result, Response)
    assert result.access_token is not None
