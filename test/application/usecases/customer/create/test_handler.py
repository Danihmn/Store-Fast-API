from http import HTTPStatus

import pytest
from fastapi import HTTPException

from application.usecases.customer.create.command import Command
from application.usecases.customer.create.handler import Handler
from application.usecases.customer.create.response import Response
from test.configuration.fake_data import CustomerFactory


async def test_handler_create_customer_success(session, customer_repository):
    # arrange
    command = Command(
        name='John Doe', email='john.doe@example.com', phone='11999999999'
    )
    handler = Handler(customer_repository)

    # act
    result = await handler.handle(command)

    # assert
    assert isinstance(result, Response)
    assert result.name == command.name
    assert result.email == command.email
    assert result.phone == command.phone


async def test_handler_create_customer_duplicate_email(
    session, customer_repository
):
    # arrange
    existing = CustomerFactory.create(email='duplicate@example.com')
    session.add(existing)
    await session.commit()

    command = Command(
        name='Jane Doe', email='duplicate@example.com', phone='11988888888'
    )
    handler = Handler(customer_repository)

    # act & assert
    with pytest.raises(HTTPException) as exc_info:
        await handler.handle(command)

    assert exc_info.value.status_code == HTTPStatus.BAD_REQUEST
    assert exc_info.value.detail == 'Customer with this email already exists'


async def test_handler_create_customer_duplicate_phone(
    session, customer_repository
):
    # arrange
    existing = CustomerFactory.create(phone='11977777777')
    session.add(existing)
    await session.commit()

    command = Command(
        name='Jane Doe', email='jane.doe@example.com', phone='11977777777'
    )
    handler = Handler(customer_repository)

    # act & assert
    with pytest.raises(HTTPException) as exc_info:
        await handler.handle(command)

    assert exc_info.value.status_code == HTTPStatus.BAD_REQUEST
    assert exc_info.value.detail == 'Customer with this phone already exists'
