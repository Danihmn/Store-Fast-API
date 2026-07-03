from http import HTTPStatus

from fastapi import HTTPException

from application.usecases.customer.delete.command import Command
from infrastructure.repositories.customer_repository import CustomerRepository


class Handler:
    def __init__(self, repository: CustomerRepository):
        self.repository = repository

    def handle(self, command: Command) -> None:
        customer = self.repository.get_customer_by_id(command.customer_id)

        if not customer:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail='Customer not found',
            )

        self.repository.delete_customer(command.customer_id)
