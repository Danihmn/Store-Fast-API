from http import HTTPStatus

from fastapi import HTTPException

from application.usecases.customer.create.command import Command
from application.usecases.customer.create.response import Response
from domain.entities.customer import Customers
from infrastructure.repositories.customer_repository import CustomerRepository


class Handler:
    def __init__(self, repository: CustomerRepository):
        self.repository = repository

    async def handle(self, command: Command) -> Response:
        existing = await self.repository.get_customer_by_email_or_phone(
            email=command.email, phone=command.phone
        )

        if existing:
            if existing.email == command.email:
                raise HTTPException(
                    status_code=HTTPStatus.BAD_REQUEST,
                    detail='Customer with this email already exists',
                )
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Customer with this phone already exists',
            )

        customer = Customers(
            name=command.name, email=command.email, phone=command.phone
        )
        created = await self.repository.create_customer(customer)

        return Response.model_validate(created)
