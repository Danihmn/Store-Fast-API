from application.usecases.customer.get_by_id.command import Command
from application.usecases.customer.get_by_id.response import Response
from infrastructure.repositories.customer_repository import CustomerRepository


class Handler:
    def __init__(self, repository: CustomerRepository):
        self.repository = repository

    async def handle(
        self,
        command: Command,
    ) -> Response:
        customer = await self.repository.get_customer_by_id(
            command.customer_id
        )

        return Response.model_validate(customer)
