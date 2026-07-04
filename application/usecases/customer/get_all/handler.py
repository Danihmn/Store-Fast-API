from application.usecases.customer.get_all.command import Command
from application.usecases.customer.get_all.response import Response
from infrastructure.repositories.customer_repository import CustomerRepository


class Handler:
    def __init__(self, repository: CustomerRepository):
        self.repository = repository

    async def handle(
        self,
        command: Command,
    ) -> list[Response]:
        customers = await self.repository.get_all_customers(
            skip=command.skip, take=command.take
        )

        return [Response.model_validate(customer) for customer in customers]
