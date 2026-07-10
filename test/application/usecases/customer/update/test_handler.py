import uuid
from http import HTTPStatus

import pytest
from fastapi import HTTPException

from application.usecases.customer.update.command import Command
from application.usecases.customer.update.handler import Handler
from application.usecases.customer.update.response import Response
from test.configuration.fake_data import CustomerFactory


async def test_handler_update_customer_success(session, customer_repository):
    # arrange
    customer = CustomerFactory.create()
    session.add(customer)
    await session.commit()

    command = Command(
        name='Updated Name',
        email='updated@example.com',
        phone='11955555555',
    )
    handler = Handler(customer_repository)

    # act
    result = await handler.handle(customer.id, command)

    # assert
    assert isinstance(result, Response)
    assert result.id == customer.id
    assert result.name == command.name
    assert result.email == command.email
    assert result.phone == command.phone


async def test_handler_update_customer_not_found(session, customer_repository):
    # arrange
    command = Command(
        name='Updated Name',
        email='updated@example.com',
        phone='11955555555',
    )
    handler = Handler(customer_repository)

    # act & assert
    with pytest.raises(HTTPException) as exc_info:
        await handler.handle(uuid.uuid4(), command)

    assert exc_info.value.status_code == HTTPStatus.NOT_FOUND
    assert exc_info.value.detail == 'Customer not found'
