from http import HTTPStatus

from fastapi import HTTPException

from application.usecases.customer.delete.command import Command
from infrastructure.repositories.customer_repository import CustomerRepository


class Handler:
    def __init__(self, repository: CustomerRepository):
        self.repository = repository

    async def handle(self, command: Command) -> None:
        deleted = await self.repository.delete_customer(command.customer_id)

        if deleted is False:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f'Customer with ID {command.customer_id} not found.',
            )
