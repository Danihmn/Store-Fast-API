import uuid
from http import HTTPStatus

from fastapi import HTTPException

from application.usecases.customer.update.command import Command
from application.usecases.customer.update.response import Response
from domain.entities.customer import Customers
from infrastructure.repositories.customer_repository import CustomerRepository


class Handler:
    def __init__(self, repository: CustomerRepository):
        self.repository = repository

    async def handle(
        self, customer_id: uuid.UUID, command: Command
    ) -> Response:
        new_customer = Customers(
            name=command.name, email=command.email, phone=command.phone
        )
        customer = await self.repository.update_customer(
            customer_id, new_customer
        )

        if not customer:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail='Customer not found',
            )

        return Response.model_validate(customer)
