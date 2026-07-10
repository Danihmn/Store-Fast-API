import uuid

import pytest
from pydantic import ValidationError

from application.usecases.customer.get_by_id.command import Command
from application.usecases.customer.get_by_id.handler import Handler
from application.usecases.customer.get_by_id.response import Response
from test.configuration.fake_data import CustomerFactory


async def test_handler_get_customer_by_id_success(session, customer_repository):
    # arrange
    customer = CustomerFactory.create()
    session.add(customer)
    await session.commit()

    command = Command(customer_id=customer.id)
    handler = Handler(customer_repository)

    # act
    result = await handler.handle(command)

    # assert
    assert isinstance(result, Response)
    assert result.id == customer.id
    assert result.email == customer.email


async def test_handler_get_customer_by_id_not_found(
    session, customer_repository
):
    # arrange
    command = Command(customer_id=uuid.uuid4())
    handler = Handler(customer_repository)

    # act & assert
    with pytest.raises(ValidationError):
        await handler.handle(command)
