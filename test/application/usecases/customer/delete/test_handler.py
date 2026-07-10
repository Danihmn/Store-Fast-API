import uuid
from http import HTTPStatus

import pytest
from fastapi import HTTPException

from application.usecases.customer.delete.command import Command
from application.usecases.customer.delete.handler import Handler
from domain.entities.customer import Customers
from test.configuration.fake_data import CustomerFactory


async def test_handler_delete_customer_success(session, customer_repository):
    # arrange
    customer = CustomerFactory.create()
    session.add(customer)
    await session.commit()

    command = Command(customer_id=customer.id)
    handler = Handler(customer_repository)

    # act
    await handler.handle(command)

    # assert
    deleted = await session.get(Customers, customer.id)
    assert deleted is None


async def test_handler_delete_customer_not_found(session, customer_repository):
    # arrange
    customer_id = uuid.uuid4()
    command = Command(customer_id=customer_id)
    handler = Handler(customer_repository)

    # act & assert
    with pytest.raises(HTTPException) as exc_info:
        await handler.handle(command)

    assert exc_info.value.status_code == HTTPStatus.NOT_FOUND
    assert (
        exc_info.value.detail
        == f'Customer with ID {customer_id} not found.'
    )
